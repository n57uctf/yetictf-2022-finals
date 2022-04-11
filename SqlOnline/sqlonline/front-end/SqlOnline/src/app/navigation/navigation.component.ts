import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../_services/auth.service';

@Component({
  selector: 'app-navigation',
  templateUrl: './navigation.component.html',
  styleUrls: ['./navigation.component.scss']
})
export class NavigationComponent implements OnInit {

  constructor(
    private auth: AuthService,
    private roter: Router,
  ) { }

  ngOnInit(): void {
    if (this.auth.authToken) {
      this.loggedOn = true;
    }
    this.auth.loggedOn.subscribe(
      res => {
        this.loggedOn = res;
      }
    )
  }

  loggedOn: boolean = false;

  logout() {
    this.auth.logout();
    this.roter.navigate(['/login']);
  }
}
