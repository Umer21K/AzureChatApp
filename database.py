from azure.cosmos.aio import CosmosClient
import os
import kv
import gemini
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Cosmos DB configuration
URL = "https://batey-db.documents.azure.com:443/"
KEY = os.environ['COSMO_KEY']
DATABASE_NAME = 'Batey'
USERS = 'User_Info'
ROOMS = 'Chat_Rooms'

# Asynchronous function to add a user
async def add_user(name, password, email):
    async with CosmosClient(URL, credential=KEY) as client:
        database = client.get_database_client(DATABASE_NAME)
        users = database.get_container_client(USERS)
    
        #  Use COUNT(*) to check if user already exists
        username_exists_query = f"SELECT VALUE COUNT(1) FROM c WHERE c.name = '{name}' OR c.email = '{email}'"

        # Execute the query and check the count
        count = 0
        async for item in users.query_items(query=username_exists_query):
            count = item

        print(count)
        
        if count == 0:
            # Query to find the highest existing ID
            query = "SELECT VALUE MAX(c.id) FROM c"
            items = users.query_items(query=query)  # Query to get the max id
            max_id = 0
            async for item in items:
                if item is not None:
                    max_id = int(item)

            # Increment the ID for the new user
            new_id = max_id + 1

            # Store the password securely in Azure Key Vault
            kv.add_client(str(new_id), password)

            # Create new user item without the password
            user_item = {
                'id': str(new_id),
                'name': name,
                'email': email
            }

            # Add the new user to the database
            await users.upsert_item(user_item)

            await create_room(str(new_id), '1')
            return user_item
        else:
            return None
    
async def create_room(User1, User2):
    async with CosmosClient(URL, credential=KEY) as client:
        database = client.get_database_client(DATABASE_NAME)
        rooms = database.get_container_client(ROOMS)
        
        # Create a unique chatroom ID regardless of message direction
        chatroom_id = f"{min(User1, User2)}_{max(User1, User2)}"

        # Query to check if the chatroom already exists using COUNT(1)
        query = f"SELECT VALUE COUNT(1) FROM c WHERE c.id = '{chatroom_id}'"
        chatroom_exists = False
        async for item in rooms.query_items(query=query):
            chatroom_exists = item > 0  # item will be the count of matching documents

        # If chatroom doesn't exist, create a new one
        if not chatroom_exists:
            chatroom = {
                'id': chatroom_id,
                'User1': User1,
                'User2': User2,
                'messages': []
            }
        
            # Update the chatroom in the database
            await rooms.upsert_item(chatroom)

async def send_message(new_message):
    async with CosmosClient(URL, credential=KEY) as client:
        database = client.get_database_client(DATABASE_NAME)
        rooms = database.get_container_client(ROOMS)

        # Create a unique chatroom ID regardless of message direction
        chatroom_id = f"{min(new_message['SenderID'], new_message['ReceiverID'])}_{max(new_message['SenderID'], new_message['ReceiverID'])}"

        # Query to check if the chatroom already exists
        query = f"SELECT * FROM c WHERE c.id = '{chatroom_id}'"
        async for item in rooms.query_items(query=query):
            chatroom = item
            # Append the new message to the chatroom's message list
            message = {
                'SenderID': new_message['SenderID'],
                'ReceiverID': new_message['ReceiverID'],
                'MessageText': new_message['MessageText'],
                'Timestamp': new_message['Timestamp']  # Current UTC timestamp
            }
            chatroom['messages'].append(message)

            # Update the chatroom in the database
            await rooms.upsert_item(chatroom)
            break


# Updated Asynchronous function to validate user
async def validate_user(password, email):
    async with CosmosClient(URL, credential=KEY) as client:
        database = client.get_database_client(DATABASE_NAME)
        users = database.get_container_client(USERS)

        if email == 'nimbus@gmail.com':
            return None

        # Query to check if the user exists with the given email
        query = f"SELECT * FROM c WHERE c.email = '{email}'"
        user_found = False
        
        
        async for item in users.query_items(query=query):
            user_found = True
            user_id = item['id']  # Retrieve user ID

            # Authenticate the password using Azure Key Vault
            if kv.authenticate(user_id, password):  # Using the authenticate function
                user_info = {
                    'userid': user_id,
                    'username': item['name'],
                    'email': item['email']
                }
                return user_info  # Return user info without the password
            else:
                return None

        if not user_found:
            return None
        
# Asynchronous function to get all other users except the specified user
async def get_other_users(userid):
    async with CosmosClient(URL, credential=KEY) as client:
        database = client.get_database_client(DATABASE_NAME)
        users = database.get_container_client(USERS)
        
        # Query to select all users except the specified userid
        query = f"SELECT * FROM c WHERE c.id != '{userid}' ORDER BY c.name ASC"
        other_users = []

        # Fetch and store all other users in the list
        async for item in users.query_items(query=query):
            user_info = {
                'userid': item['id'],
                'username': item['name']
            }
            other_users.append(user_info)

        return other_users  # Return the list of other user objects

# Asynchronous function to get all other users except the specified user
async def get_rooms(userid):
    async with CosmosClient(URL, credential=KEY) as client:
        database = client.get_database_client(DATABASE_NAME)
        users = database.get_container_client(USERS)
        rooms = database.get_container_client(ROOMS)
        
        # Query to select all users except the specified userid
        query = f"SELECT * FROM c WHERE c.User1 = '{userid}' OR c.User2 = '{userid}'"
        rooms_data = []

        # Fetch and store all other users in the list
        async for item in rooms.query_items(query=query):
            room_info = {
                'id': item['id'],
                'User1': item['User1'],
                'User2': item['User2']
            }
            rooms_data.append(room_info)

        # Fetch all users for a manual join
        query_users = f"SELECT c.id, c.name FROM c WHERE c.id != '{userid}'"
        users_dict = {}
        async for item in users.query_items(query=query_users):
            users_dict[item['id']] = item['name']

        rooms = []
         # Combine room data with user names
        for room in rooms_data:
            # Try to fetch names for User1 and User2
            name1 = users_dict.get(room['User1'], "Unknown")  # Default to "Unknown" if not found
            name2 = users_dict.get(room['User2'], "Unknown")

            # Choose a name to display and set the other user id
            if name1 != "Unknown":
                room['name'] = name1
                other_userid = room['User1']
            else:
                room['name'] = name2
                other_userid = room['User2']

            rooms.append({'roomid': room['id'], 'roomname': room['name'], 'userid': other_userid})
        rooms = sorted(rooms, key=lambda d: d['roomname'])
        
        return rooms

async def get_messages(room_id):
    async with CosmosClient(URL, credential=KEY) as client:
        database = client.get_database_client(DATABASE_NAME)
        rooms = database.get_container_client(ROOMS)
        
        # Query to find the chatroom by ID
        query = f"SELECT * FROM c WHERE c.id = '{room_id}'"
        
        chatroom_data = None
        async for item in rooms.query_items(query=query):
            chatroom_data = item  # Store the chatroom data

        # Extract messages if chatroom exists
        if chatroom_data and "messages" in chatroom_data:
            # Sort messages by Timestamp (earliest first)
            sorted_messages = sorted(
                chatroom_data["messages"],
                key=lambda x: x["Timestamp"]
            )
            return sorted_messages  # Return sorted messages
        else:
            return []

async def chat_with_nimbus(new_message):
    async with CosmosClient(URL, credential=KEY) as client:
        database = client.get_database_client(DATABASE_NAME)
        rooms = database.get_container_client(ROOMS)

        # Create a unique chatroom ID regardless of message direction
        chatroom_id = f"{min(new_message['SenderID'], new_message['ReceiverID'])}_{max(new_message['SenderID'], new_message['ReceiverID'])}"

        gemini_response = gemini.nimbus(new_message['MessageText'])

        # Append the new message to the chatroom's message list
        message = {
            'SenderID': new_message['SenderID'],
            'ReceiverID': new_message['ReceiverID'],
            'MessageText': new_message['MessageText'],
            'Timestamp': new_message['Timestamp']  # Current UTC timestamp
        }

        nimbus_message = {
                # new message sender is now receiver
                'SenderID': new_message['ReceiverID'],
                'ReceiverID': new_message['SenderID'],
                'MessageText': gemini_response,
                'Timestamp': new_message['Timestamp'] # Current UTC timestamp
            }

        # Query to check if the chatroom already exists
        query = f"SELECT * FROM c WHERE c.id = '{chatroom_id}'"
        async for item in rooms.query_items(query=query):
            chatroom = item
            chatroom['messages'].append(message)
            chatroom['messages'].append(nimbus_message)

            # Update the chatroom in the database
            await rooms.upsert_item(chatroom)
            break