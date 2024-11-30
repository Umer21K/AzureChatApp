import { AlertService } from '../services/alert.service';
import { UserService } from '../services/user.service';
import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { playKeyboardSound } from '../util/audio';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrl: './register.component.css'
})

export class RegisterComponent {
  registerForm: FormGroup = this.fb.group({
    name: ['', { validators: [Validators.required, Validators.maxLength(25)] }],
    email: ['', { validators: [Validators.required, Validators.maxLength(25), Validators.email] }],
    password: ['', { validators: [Validators.required, Validators.minLength(8)] }],
    confirmPassword: ['', { validators: [Validators.required, Validators.minLength(8)] }]
  });

  // regsiterFailed

  constructor(private fb: FormBuilder, private router: Router, private userService: UserService, private alertService: AlertService) { }

  ngOnInit() {
    if (localStorage.getItem('user')) {
      this.router.navigate(['chat-page']);
    }
  }

  async register() {
    playKeyboardSound();

    if (this.registerForm.valid) {
      const data = this.registerForm.value;
      const { name, email, password, confirmPassword } = data;

      if (password !== confirmPassword) {
        this.alertService.emitErrorEvent('Error', 'Passwords do not match');
        return;
      }


      const response: any = await this.userService.register(name, email, password);
      if (response.success) {
        const userid = response.userid;

        localStorage.setItem('userid', JSON.stringify(userid));
        this.router.navigate(['chat-page']);
      }
      else {
        this.alertService.emitErrorEvent('Error', response.message);
        return;
      }
    }
  }

  back() {
    playKeyboardSound();
    this.router.navigate(['home']);
  }
}