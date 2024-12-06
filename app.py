from flask_socketio import SocketIO, join_room, leave_room, emit
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from blob_storage import *
from database import *
import os



app = Flask(__name__, static_folder='static', template_folder='static')
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet', logger=True, engineio_logger=True)
CORS(app)  # Enable CORS for frontend-backend communication

def handle_error(message, error, status_code=500):
    app.logger.error(f"{message}: {error}")
    return jsonify({'success': False, 'message': 'An unexpected error occurred. Please try again later.'}), status_code

@app.route('/')
@app.route('/<path:path>')
def serve_angular(path=None):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/add_user', methods=['POST'])
async def add_user_api():
    try:
        data = request.json
        name = data.get('name')
        password = data.get('password')
        email = data.get('email')

        user_info = await add_user(name, password, email)
        
        if user_info:
            return jsonify({'success': True, 'userid': user_info['id'], 'username': user_info['name']}), 201
        else:
            return jsonify({'success': False, 'message': 'User already exists with that name or email'}), 200
    except Exception as e:
        return handle_error("Error adding user", e)

@app.route('/validate_user', methods=['POST'])
async def validate_user_api():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        user_info = await validate_user(password, email)
        
        if user_info:
            return jsonify({'success': True, 'userid': user_info['userid'], 'username': user_info['username']}), 200
        else:
            return jsonify({'success': False,'message': 'Invalid credentials'}), 200
    except Exception as e:
        return handle_error("Error validating user", e)

@app.route('/get_other_users/<userid>', methods=['GET'])
async def get_other_users_api(userid):
    try:
        users = await get_other_users(userid)

        # Return success response
        return jsonify({'success': True, 'data': users}), 200
    except Exception as e:
        # Log the error for debugging
        app.logger.error(f"Error fetching other users for userid {userid}: {e}")
        
        return handle_error("Error getting users", e)

@app.route('/get_rooms/<userid>', methods=['GET'])
async def get_rooms_api(userid):
    try:
        # Fetch rooms for the given user ID
        rooms = await get_rooms(userid)

        # Return success response with room data
        return jsonify({'success': True, 'data': rooms}), 200
    except Exception as e:
        # Log the error for debugging
        app.logger.error(f"Error fetching rooms for user {userid}: {e}")

        # Return a generic error message
        return handle_error("Error getting rooms", e)


@app.route('/get_messages/<roomid>', methods=['GET'])
async def get_messages_api(roomid):
    try:
        messages = await get_messages(roomid)

        return jsonify({'success': True, 'data': messages}), 200
    except Exception as e:
        # Log the error for debugging
        app.logger.error(f"Error fetching messages for user {roomid}: {e}")

        # Return a generic error message
        return handle_error("Error getting messages", e)

@app.route('/create_room', methods=['POST'])
async def create_room_api():
    try:
        data = request.json
        User1 = data['User1']
        User2 = data['User2']

        await create_room(User1, User2)
        
        return jsonify({'success': True, 'message': 'Chat created successfuly'}),  201
    except Exception as e:# Log the error for debugging
        app.logger.error(f"Error creating room for user {User1} and user 2 {User2}: {e}")

        # Return a generic error message
        return handle_error("Error creating room", e)

@app.route('/send_message', methods=['POST'])
async def send_message_api():
    try:
        data = request.json
        message = data['message']
        await send_message(message)

        return jsonify({'success': True, 'message': 'Message sent successfuly'}),  201
    except Exception as e:
        app.logger.error(f"Error sending message {message}: {e}")

        # Return a generic error message
        return handle_error("Error sending message", e)

@app.route('/send_message_nimbus', methods=['POST'])
async def send_message_nimbus_api():
    try:
        data = request.json
        message = data['message']
        await chat_with_nimbus(message)
        return jsonify({'success': True, 'message': 'Message sent successfuly'}),  201
    except Exception as e:
        app.logger.error(f"Error sending message {message} to nimbus: {e}")

        # Return a generic error message
        return handle_error("Error sending message to nimbus", e)

@app.route('/send_file', methods=['POST'])
async def send_file_api():
    try:
        room_id = request.form.get('roomid')  # Get the room ID from the form
        file = request.files['file']  # Get the uploaded file
        file_name = file.filename  # Extract the file name
        file_data = file.read()  # Read the file content

        # Call the Azure function to upload the file
        await send_file(room_id, file_data, file_name)

        return jsonify({'success': True, 'message': 'Image sent successfully'}), 201
    except Exception as e:
        app.logger.error(f"Error sending file {file}: {e}")

        # Return a generic error message
        return handle_error("Error sending file", e)

@app.route('/get_files/<room_id>', methods=['GET'])
async def get_files_api(room_id):
    try:
        # Call the Azure function to get files
        files = await get_files(room_id)
        return jsonify({'success': True, 'files': files}), 200
    except Exception as e:
        app.logger.error(f"Error getting files in room {room_id}: {e}")

        # Return a generic error message
        return handle_error("Error getting file", e)

@socketio.on('message')
def handle_message(data):
    message = data['message']
    room = data['room']
    sender_name = data['senderName']

    # Emit the message back to all clients in the room
    emit('message', {'message': message, 'room': room, 'senderName': sender_name }, to=room)

@socketio.on('join_room')
def handle_join_room(data):
    room = data['room']
    join_room(room)

@socketio.on('leave_room')
def handle_leave_room(data):
    room = data['room']
    leave_room(room)

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=8000)
