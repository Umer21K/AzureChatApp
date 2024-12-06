import os
from azure.identity import ClientSecretCredential
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client_id = os.environ['AZURE_CLIENT_ID']
tenant_id = os.environ['AZURE_TENANT_ID']
client_secret = os.environ['AZURE_CLIENT_SECRET']
account_url = os.environ["AZURE_STORAGE_URL"]

# Create a credential
credentials = ClientSecretCredential(
    client_id=client_id,
    client_secret=client_secret,
    tenant_id=tenant_id
)

# BlobServiceClient
blob_service_client = BlobServiceClient(account_url=account_url, credential=credentials)

async def send_file(room_id, file_data, file_name):
    """
    Creates a container with the name `room_id` if it doesn't exist
    and uploads the file to that container.
    """
    # Replace underscores with hyphens and ensure room_id is lowercase
    room_id = str(room_id).replace('_', '-').lower()

    # Get the container client
    container_client = blob_service_client.get_container_client(room_id)

    try:
        # Create container if it does not exist
        if not container_client.exists():
            print(f"Creating container: {room_id}")
            container_client.create_container()
            container_client.set_container_access_policy(public_access='blob', signed_identifiers={})

        # Upload file to the container
        container_client.upload_blob(name=file_name, data=file_data)
        print(f"File {file_name} uploaded to container {room_id}.")
    except Exception as e:
        print(f"Error in Azure upload: {e}")

async def get_files(room_id):
    """
    Retrieves all files from the container named `room_id`.
    """
    # Sanitize the room_id for Azure Blob Storage
    room_id = str(room_id).replace('_', '-').lower()

    try:
        # Initialize the BlobServiceClient
        blob_service_client = BlobServiceClient(account_url=account_url, credential=credentials)

        # Get the container client
        container_client = blob_service_client.get_container_client(room_id)

        # Check if the container exists
        if not container_client.exists():
            print(f"Container {room_id} does not exist.")
            return []

        # List blobs in the container
        blobs = container_client.list_blobs()
        files = [
            {
                'name': blob.name,
                'url': f"{container_client.url}/{blob.name}"  # Construct file URL
            }
            for blob in blobs
        ]
        
        files.reverse()

        # If the container is empty, return an empty list
        if not files:
            print(f"Container {room_id} is empty.")
            return []

        return files

    except Exception as e:
        print(f"Error retrieving files from {room_id}: {e}")
        return []