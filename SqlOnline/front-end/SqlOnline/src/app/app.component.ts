import { Component, OnInit } from '@angular/core';
import { AuthService } from './_services/auth.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  title = 'SqlOnline';

  constructor(private auth: AuthService) { }

  ngOnInit() {
    if (this.auth.authToken) {
      this.auth.loggedOn.next(true);
    }
  }
}
