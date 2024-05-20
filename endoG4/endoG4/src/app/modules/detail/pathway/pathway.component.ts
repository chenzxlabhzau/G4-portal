import { Component, OnInit, Input, ViewChild, SimpleChanges, OnChanges} from '@angular/core';
import { MatPaginator } from "@angular/material/paginator";
import { MatSort } from "@angular/material/sort";
import {MatTableDataSource} from "@angular/material/table";

@Component({
  selector: 'app-pathway',
  templateUrl: './pathway.component.html',
  styleUrls: ['./pathway.component.css']
})
export class PathwayComponent implements OnInit, OnChanges {
  dataSource: MatTableDataSource<any>
  @Input() pathwayRecord
  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;
  displayedColumns = ['tf','pathway_name','ec'];
  constructor() { }

  ngOnInit(): void {
  }
  ngOnChanges(changes: SimpleChanges) {
  if (changes.pathwayRecord && changes.pathwayRecord.currentValue) {
    this.dataSource = new MatTableDataSource(this.pathwayRecord);
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
  }
}
}
