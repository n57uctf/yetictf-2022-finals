import { Component, OnInit } from '@angular/core';
import { AuthService } from '../_services/auth.service';
import { Response } from '../_models/Response';
import { UserCreds } from '../_models/UserCreds';

@Component({
  selector: 'app-registration',
  templateUrl: './registration.component.html',
  styleUrls: ['./registration.component.scss']
})
export class RegistrationComponent {

  constructor(private auth: AuthService) { }

  message:string = "";

  register(login:string, password:string, password2:string) {
    this.message = "";
    if (password != password2) {
      this.message = "Passwords didn't match";
    } else {
      let cred: UserCreds = {
        login: login,
        password: password
      }
      
      this.auth.registration(
        cred
      ).subscribe(
        (response: Response) => {
          if (response.success == false) {
            this.message = "Error";
          } else {
            this.message = "Success";
          }
        }
      )
    }
  }

}
