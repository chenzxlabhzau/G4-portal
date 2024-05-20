import {Component, Input, OnChanges, OnInit, ViewChild, SimpleChanges} from '@angular/core';
import {MatTableDataSource} from "@angular/material/table";
import {MatPaginator} from "@angular/material/paginator";
import {MatSort} from "@angular/material/sort";

@Component({
  selector: 'app-sample',
  templateUrl: './sample.component.html',
  styleUrls: ['./sample.component.css']
})
export class SampleComponent implements OnInit, OnChanges {
  dataSource
  @Input() SampleData: any;
  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;
  displayedColumns: string[] = ["sample","cell_line", "treat", "source", "gse"]
  constructor() { }

  ngOnInit(): void {
  }
  ngOnChanges(changes: SimpleChanges) {
    this.dataSource = new MatTableDataSource(this.SampleData);
    this.dataSource.paginator = this.paginator
    this.dataSource.sort = this.sort
  }
}
