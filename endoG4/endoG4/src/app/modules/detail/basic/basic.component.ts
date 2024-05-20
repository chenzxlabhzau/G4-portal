import { Component, OnInit, Input } from '@angular/core';
import { Basicrecord } from "../../../shared/model/basic";
import { ActivatedRoute } from "@angular/router";

@Component({
  selector: 'app-basic',
  templateUrl: './basic.component.html',
  styleUrls: ['./basic.component.css']
})
export class BasicComponent implements OnInit {
  @Input() g4info:Basicrecord
  isshow: boolean
  constructor(private route: ActivatedRoute) {
    this.route.params.subscribe((params) => {
      this.isshow = params.g_id.startsWith("HG4");
  })
  }

  ngOnInit(): void {
  }

}
