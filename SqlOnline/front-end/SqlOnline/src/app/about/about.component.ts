import { Component, OnInit } from '@angular/core';
import { Response } from '../_models/Response';
import { ApiService } from '../_services/api.service';

@Component({
  selector: 'app-about',
  templateUrl: './about.component.html',
  styleUrls: ['./about.component.scss']
})
export class AboutComponent implements OnInit {

  constructor(private api: ApiService) { }

  newDbs: any = [];

  ngOnInit(): void {
  
    this.api.lastDbs(600).subscribe(
      (data: Response) => {
        if (data.success) {
          this.newDbs = data.data;
        }
      }
    )
  }
}
