import { Component, OnInit } from '@angular/core';
import { Response } from '../_models/Response';
import { ApiService } from '../_services/api.service';

@Component({
  selector: 'app-docs',
  templateUrl: './docs.component.html',
  styleUrls: ['./docs.component.scss']
})
export class DocsComponent implements OnInit {

  constructor(private api: ApiService) { }

  userApiKey = "";

  ngOnInit(): void {
    this.api.getUserApiKey().subscribe(
      (data: Response) => {
        if (data.success) {
          this.userApiKey = data.data.apikey;
        } else {
          this.userApiKey = "";
        }
      }
    )
  }

}
