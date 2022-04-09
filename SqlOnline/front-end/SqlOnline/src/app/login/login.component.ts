import { Component, OnInit } from '@angular/core';
import { AuthService } from '../_services/auth.service';
import { AuthToken } from '../_models/AuthToken';
import { Response } from '../_models/Response';
import { UserCreds } from '../_models/UserCreds';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {

  constructor(private auth: AuthService, private router: Router) { }

  message: string = "";

  login(login: string, password: string) {
    let cred: UserCreds = {
      login: login,
      password: password,
    }
    this.auth.login(
      cred
    ).subscribe(
      (data: Response) => {
        if (data.success) {
          this.auth.updateToken(data.data);
          this.router.navigate(["/"]);
        } else {
          this.message = "Wrong login or password";
        }
      }
    )
  }

}
