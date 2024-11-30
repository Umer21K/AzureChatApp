import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { ChatPageComponent } from './chat-page/chat-page.component';
import { LoginComponent } from './login/login.component';
import { HomeComponent } from './home/home.component';
import { RegisterComponent } from './register/register.component';
import { AuthGuard } from './services/auth-guard.guard';

const routes: Routes = [
  {
    path: 'home',
    title: 'Welcome to باتیں',
    component: HomeComponent,
  },
  {
    path: 'login',
    title: 'Login | باتیں',
    component: LoginComponent,
  },
  {
    path: 'register',
    title: 'Register | باتیں',
    component: RegisterComponent,
  },
  {
    path: 'chat-page',
    title: 'Chat Page | باتیں',
    component: ChatPageComponent,
    canActivate: [AuthGuard]
  },
  { path: '', redirectTo: '/home', pathMatch: 'full' }, // default route
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
