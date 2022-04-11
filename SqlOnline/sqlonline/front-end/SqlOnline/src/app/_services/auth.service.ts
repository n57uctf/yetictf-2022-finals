import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, Subject, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';
import { Response } from '../_models/Response';
import { UserCreds } from '../_models/UserCreds';
import { environment } from 'src/environments/environment';
import { AuthToken } from '../_models/AuthToken';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor(private http: HttpClient) { }

  serverUrl = document.location.protocol + "//" + document.location.host;

  loggedOn: Subject<boolean> = new Subject();
  authToken: string | null = localStorage.getItem("jwt");

  public registration(creds: UserCreds): Observable<Response> {
    return this.http.post<Response>(
      this.serverUrl + "/register",
      creds,
    )
  }

  public login(creds: UserCreds): Observable<Response> {
    return this.http.post<Response>(
      this.serverUrl + "/login",
      creds,
    )
  }

  public logout() {
    localStorage.removeItem("jwt");
    this.loggedOn.next(false);
  }

  public updateToken(jwt: AuthToken) {
    this.authToken = jwt.jwt;
    localStorage.setItem("jwt", jwt.jwt);
    this.loggedOn.next(true);
  }

}
