import { AlertService } from '../services/alert.service';
import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { playKeyboardSound } from '../util/audio';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { UserService } from '../services/user.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrl: './login.component.css',
})
export class LoginComponent {
  loginForm: FormGroup = this.fb.group({
    email: ['', { validators: [Validators.required] }],
    password: ['', { validators: [Validators.required] }],
  });

  loginSuccess: Boolean = true;

  constructor(private fb: FormBuilder, private router: Router, private userService: UserService, private alertService: AlertService) { }
  ngOnInit() {
    if (localStorage.getItem('user')) {
      this.router.navigate(['chat-page']);
    }
  }

  async login() {
    playKeyboardSound();
    const { email, password } = this.loginForm.value;

    if (email && password) {
      const response = await this.userService.login(email, password);

      if (response.success) {
        const userid = response.userid;
        localStorage.setItem('userid', JSON.stringify(userid));
        this.loginForm.reset();
        this.router.navigate(['chat-page']);
      }
      else {
        this.alertService.emitErrorEvent('Error', response.message);
      }
    }
  }

  back(): void {
    playKeyboardSound();
    this.router.navigate(['home']);
  }
}
