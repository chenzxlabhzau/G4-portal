import { Component, OnInit, Input, ViewChild, SimpleChanges, OnChanges} from '@angular/core';
import { MatPaginator } from "@angular/material/paginator";
import { MatSort } from "@angular/material/sort";
import {MatTableDataSource} from "@angular/material/table";

@Component({
  selector: 'app-tf',
  templateUrl: './tf.component.html',
  styleUrls: ['./tf.component.css']
})
export class TfComponent implements OnInit, OnChanges {
  dataSource: MatTableDataSource<any>
  @Input() tfRecord
  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;
  displayedColumns = ['tf','tfloci','score','match_seq'];
  constructor() {
  }

  ngOnInit(): void {
  }
  ngOnChanges(changes: SimpleChanges) {
  if (changes.tfRecord && changes.tfRecord.currentValue) {
    this.dataSource = new MatTableDataSource(this.tfRecord);
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
  }
}

}
