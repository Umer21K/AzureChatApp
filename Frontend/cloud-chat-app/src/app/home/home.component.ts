import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { playKeyboardSound } from '../util/audio';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {
  constructor(private router: Router) { }

  ngOnInit() {
    if (localStorage.getItem('user')) {
      this.router.navigate(['chat-page']);
    }
  }

  login() {
    playKeyboardSound();
    this.router.navigate(['login']);
  }

  register() {
    playKeyboardSound();
    this.router.navigate(['register']);
  }
}
