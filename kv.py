from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

client_id = os.environ['AZURE_CLIENT_ID']
tenant_id = os.environ['AZURE_TENANT_ID']
client_secret = os.environ['AZURE_CLIENT_SECRET']
vault_url = os.environ['AZURE_VAULT_URL']

# Create a credential
credentials = ClientSecretCredential(
    client_id=client_id,
    client_secret=client_secret,
    tenant_id=tenant_id
)

# Create a secret client object
secret_client = SecretClient(vault_url=vault_url, credential=credentials)

# Function 1: Add a client
def add_client(user_id, user_password):
    """
    Adds a client to Azure Key Vault.
    
    Args:
        user_id (str): The user ID, used as the secret name.
        user_password (str): The user password, used as the secret value.
    """
    try:
        secret_client.set_secret(user_id, user_password)
        # print(f"Secret '{user_id}' added successfully.")
    except Exception as e:
        pass
        # print(f"Failed to add secret '{user_id}': {e}")

# Function 2: Authenticate a client
def authenticate(user_id, user_password):
    """
    Authenticates a client by verifying the provided password against the stored secret.
    
    Args:
        user_id (str): The user ID, used as the secret name.
        user_password (str): The user password to authenticate.
    
    Returns:
        bool: True if authentication is successful, False otherwise.
    """
    try:
        # Retrieve the secret
        secret = secret_client.get_secret(user_id)
        # Compare the provided password with the stored secret value
        if secret.value == user_password:
            return True
        else:
            return False
    except Exception as e:
        return False
