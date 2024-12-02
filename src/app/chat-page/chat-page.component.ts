import { ToastrService } from 'ngx-toastr';
import { AlertService } from './../services/alert.service';
import { ChatService } from '../services/chat.service';
import { Message } from '../models/message.model';
import { Component, ElementRef, OnDestroy, ViewChild } from '@angular/core';
import { playKeyboardSound, notificationSound } from "../util/audio";
import { Room } from '../models/room.model';
import { Router } from '@angular/router';
import { User } from '../models/user.model';
import { Socket } from 'ngx-socket-io';

@Component({
  selector: 'app-chat-page',
  templateUrl: './chat-page.component.html',
  styleUrl: './chat-page.component.css'
})
export class ChatPageComponent implements OnDestroy {
  searchChat: String = '';
  searchNewChat: String = '';
  messageText: String = '';

  messages: Message[] = [];
  chats: Room[] = [];

  selectedChat: Room = { roomid: '-1', roomname: '', userid: '-1' };
  currentUserId: String = JSON.parse(localStorage.getItem('userid') || '0');

  searchNewChatId: String = '';
  showNewChatPopup = false;
  selectedNewChatId: String = '-1';
  selectedNewChatName: String = '';

  allUsers: User[] = [];

  @ViewChild('scrollableDiv') scrollableDiv!: ElementRef;

  constructor(private socket: Socket, private router: Router, private chatService: ChatService, private alertService: AlertService, private toastrService: ToastrService) { }

  async ngOnInit() {
    let selected: Room = JSON.parse(localStorage.getItem('selectedUser') || '0');

    this.chats = await this.chatService.getRooms();
    this.messages = await this.chatService.getMessages();

    if (selected) {
      this.selectedChat = selected;
      this.socket.emit('join_room', { room: this.selectedChat.roomid });
      this.socket.fromEvent('message').subscribe((message: any) => {
        const m = message.message;

        this.messages.push(m);

        if (m.SenderID !== this.currentUserId) {
          notificationSound();
          this.alertService.toaster('success', 'Message from ' + this.selectedChat.roomname, m.MessageText, 3000);
        }
      });
    };
  };

  async selectChat(chat: Room) {
    playKeyboardSound();
    this.selectedChat = { roomid: chat.roomid, roomname: chat.roomname, userid: chat.userid };
    localStorage.setItem('selectedUser', JSON.stringify(this.selectedChat));

    this.messages = await this.chatService.getMessages();
  }

  async sendMessage() {
    if (this.messageText.trim()) {
      playKeyboardSound();
      const message = { SenderID: this.currentUserId, ReceiverID: this.selectedChat.userid, MessageText: this.messageText }
      this.messageText = '';

      if (message.ReceiverID != '1') {
        this.socket.emit('message', { message, room: this.selectedChat.roomid });
        this.chatService.sendMessage(message);
      }
      else {
        await this.chatService.sendToNimbus(message);
        this.messages = await this.chatService.getMessages();
      }

    }
  }

  async newChat() {
    playKeyboardSound();
    this.showNewChatPopup = !this.showNewChatPopup;

    if (this.showNewChatPopup) {
      this.allUsers = await this.chatService.getAllUsers();
    }
    else {
      this.selectedNewChatId = '-1';
      this.selectedNewChatName = '';
    }
  }

  selectNewUser(user: User) {
    playKeyboardSound();
    this.selectedNewChatId = user.userid;
    this.selectedNewChatName = user.username;
  }

  async createNewChat() {
    playKeyboardSound();
    await this.chatService.createRoom(this.selectedNewChatId);
    this.chats = await this.chatService.getRooms();
    this.selectedNewChatId = '-1';
    this.selectedNewChatName = '';
    this.showNewChatPopup = false;
  }

  logOut() {
    playKeyboardSound();
    localStorage.clear();
    this.router.navigate(['home']);
  }

  ngAfterViewChecked() {
    this.scrollToBottom();
  }

  scrollToBottom() {
    if (this.scrollableDiv) {
      const element = this.scrollableDiv.nativeElement;
      element.scrollTop = element.scrollHeight;
    }

  }

  ngOnDestroy() {
    this.socket.emit('leave_room', { room: this.selectedChat.roomid });
  }
}
