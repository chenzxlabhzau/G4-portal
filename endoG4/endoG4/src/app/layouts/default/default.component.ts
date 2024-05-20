import { Component, OnInit } from '@angular/core';
import { Router, RouterEvent, RouteConfigLoadStart, RouteConfigLoadEnd } from '@angular/router';

@Component({
  selector: 'app-default',
  templateUrl: './default.component.html',
  styleUrls: ['./default.component.css']
})
export class DefaultComponent implements OnInit {

  loading: boolean

  constructor(router: Router) {
    this.loading = false;
    // @ts-ignore
    router.events.subscribe((event:RouterEvent): void=> {
      if (event instanceof RouteConfigLoadStart) {
        this.loading = true;
      } else if (event instanceof RouteConfigLoadEnd) {
        this.loading = false;
      }
    });
  }
  ngOnInit(): void {
  }

}
