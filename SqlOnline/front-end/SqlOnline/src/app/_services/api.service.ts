import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Response } from '../_models/Response';
import { AuthService } from './auth.service';
import { environment } from 'src/environments/environment';
import { DBDatabase } from '../_models/DBDatabase';


@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private api: HttpClient, private auth: AuthService) { }

  serverUrl = document.location.protocol + "//" + document.location.host;

  lastDbs(seconds: number): Observable<Response> {
    return this.api.get<Response>(
      this.serverUrl + '/last_log?seconds=' + seconds,
    )
  }

  getUserApiKey() {
    return this.api.get<Response>(
      this.serverUrl + '/api_key',
      {headers: {"Authorization": `Bearer ${this.auth.authToken}`}}
    )
  }

  getUserDbs() {
    return this.api.get<Response>(
      this.serverUrl + '/dbs',
      {headers: {"Authorization": `Bearer ${this.auth.authToken}`}}
    )
  }

  createNewDB(schema: DBDatabase) {
    return this.api.post<Response>(
      this.serverUrl + '/new_db',
      schema,
      {headers: {"Authorization": `Bearer ${this.auth.authToken}`}}
    )
  }

}
