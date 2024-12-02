import { lastValueFrom } from 'rxjs';
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})

export class UserService {
  private url = 'http://127.0.0.1:8080/';

  constructor(private http: HttpClient) { }

  login(email: String, password: String): any {
    return lastValueFrom(
      this.http.post
        (this.url + 'validate_user',
          { email, password })
    );
  }

  register(name: String, email: String, password: String) {
    return lastValueFrom(
      this.http.post
        (this.url + 'add_user',
          { name, email, password })
    );
  }
}