import { Component, OnInit } from '@angular/core';
import GenomeVersion from "../../../shared/constants/GenomeVersion";


@Component({
  selector: 'app-version',
  templateUrl: './version.component.html',
  styleUrls: ['./version.component.css']
})

export class VersionComponent implements OnInit {
  displayedColumns: string[] = ['species', 'Scientific_name', 'version'];
  dataSource = GenomeVersion;
  constructor() { }

  ngOnInit(): void {
  }

}
