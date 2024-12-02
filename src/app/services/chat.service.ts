import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { User } from '../models/user.model';
import { Room } from '../models/room.model';
import { lastValueFrom, Observable } from 'rxjs';
import { Message } from '../models/message.model';

@Injectable({
    providedIn: 'root'
})

export class ChatService {
    private url = 'http://127.0.0.1:8080/';

    constructor(private http: HttpClient) { }

    getRooms(): any {
        const userid: User = JSON.parse(localStorage.getItem('userid') || '0');

        return lastValueFrom(
            this.http.get<Room[]>
                (this.url + 'get_rooms/' + userid)
        );
    }

    createRoom(User2: String): any {
        const User1 = JSON.parse(localStorage.getItem('userid') || '0');

        return lastValueFrom(
            this.http.post
                (this.url + 'create_room', { User1, User2 })
        );
    }

    getAllUsers(): any {
        const userid: User = JSON.parse(localStorage.getItem('userid') || '0');

        return lastValueFrom(
            this.http.get<User[]>
                (this.url + 'get_other_users/' + userid)
        );
    }

    getMessages(): any {
        const selectedUser: Room = JSON.parse(localStorage.getItem('selectedUser') || '0');
        const room_id = selectedUser.roomid;

        return lastValueFrom(
            this.http.get<Message[]>
                (this.url + 'get_messages/' + room_id)
        );
    }

    sendMessage(message: any): any {
        return lastValueFrom(
            this.http.post
                (this.url + 'send_message', { message })
        );
    }

    sendToNimbus(message: any): any {
        return lastValueFrom(
            this.http.post
                (this.url + 'send_message_nimbus', { message })
        );
    }
}