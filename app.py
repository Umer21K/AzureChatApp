from flask_socketio import SocketIO, join_room, leave_room, emit
from flask import Flask, request, jsonify
from flask_cors import CORS
from database_finalized import *  # Import all async functions

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Initialize Socket.IO with Flask
CORS(app)  # Enable CORS for frontend-backend communication

@app.route('/add_user', methods=['POST'])
async def add_user_api():
    try:
        data = request.json
        name = data.get('name')
        password = data.get('password')
        email = data.get('email')
        user_info = await add_user(name, password, email)
        if user_info:
            return jsonify({'success': True, 'userid': user_info['id']}), 201
        else:
            return jsonify({'success': False, 'message': 'User already exists with that name or email'}), 200
    except Exception as e:
        return jsonify(f"Something went wrong: {e}. Please contact the devs ;(")

@app.route('/validate_user', methods=['POST'])
async def validate_user_api():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        user_info = await validate_user(password, email)
        if user_info:
            return jsonify({'success': True, 'userid': user_info['userid']}), 200
        else:
            return jsonify({'success': False,'message': 'Invalid credentials'}), 200
    except Exception as e:
        return jsonify(f"Something went wrong: {e}. Please contact the devs ;(")

@app.route('/get_other_users/<userid>', methods=['GET'])
async def get_other_users_api(userid):
    try:
        users = await get_other_users(userid)
        # return jsonify({'users': users}), 200
        return jsonify(users), 200
    except Exception as e:
        return jsonify(f"Something went wrong: {e}. Please contact the devs ;(")

@app.route('/get_rooms/<userid>', methods=['GET'])
async def get_rooms_api(userid):
    try:
        rooms = await get_rooms(userid)
        # return jsonify({'users': users}), 200
        return jsonify(rooms), 200
    except Exception as e:
        return jsonify(f"Something went wrong: {e}. Please contact the devs ;(")

@app.route('/get_messages/<roomid>', methods=['GET'])
async def get_messages_api(roomid):
    try:
        messages = await get_messages(roomid)
        # return jsonify({'messages': messages}), 200
        return jsonify(messages), 200
    except Exception as e:
        return jsonify(f"Something went wrong: {e}. Please contact the devs ;(")

@app.route('/create_room', methods=['POST'])
async def create_room_api():
    try:
        data = request.json
        User1 = data['User1']
        User2 = data['User2']
        await create_room(User1, User2)
        return jsonify({'message': 'Chat created successfuly'}),  200
    except Exception as e:
        return jsonify(f"Something went wrong: {e}. Please contact the devs ;(")

@app.route('/send_message', methods=['POST'])
async def send_message_api():
    try:
        data = request.json
        message = data['message']
        await send_message(message)

        return jsonify({'message': 'Message sent successfuly'}),  200
    except Exception as e:
        return jsonify(f"Something went wrong: {e}. Please contact the devs ;(")

@app.route('/send_message_nimbus', methods=['POST'])
async def send_message_nimbus_api():
    try:
        data = request.json
        message = data['message']
        await chat_with_nimbus(message)
        return jsonify({'message': 'Message sent successfuly'}),  200
    except Exception as e:
        return jsonify(f"Something went wrong: {e}. Please contact the devs ;("), 500

@socketio.on('message')
def handle_message(data):
    message = data['message']
    room = data['room']

    message.update({
        'Timestamp': datetime.utcnow().isoformat()
    })

    # Emit the message back to all clients in the room
    emit('message', {'message': message}, room=room)

@socketio.on('join_room')
def handle_join_room(data):
    room = data['room']
    join_room(room)

@socketio.on('leave_room')
def handle_leave_room(data):
    room = data['room']
    leave_room(room)

if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0', port=8080)