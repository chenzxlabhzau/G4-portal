import {Component, OnInit, Input, ViewChild, AfterViewInit, SimpleChanges, OnChanges} from '@angular/core';
import { MatPaginator } from "@angular/material/paginator";
import { MatSort } from "@angular/material/sort";
import {MatTableDataSource} from "@angular/material/table";
import {MatTableExporterDirective} from "mat-table-exporter";

@Component({
  selector: 'app-eqtl-table',
  templateUrl: './eqtl-table.component.html',
  styleUrls: ['./eqtl-table.component.css']
})
export class EqtlTableComponent implements OnInit, OnChanges {
  eqtldataSource
  g_id: string
  @Input() data: any;
  @ViewChild(MatTableExporterDirective, { static: false }) exporter: MatTableExporterDirective;
  @Input() eqtlType:string;
  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;
  displayedColumns = ['rsid', 'cloci', 'phenotype'];
  exportTable() {
  this.exporter.exportTable('csv');
  }
  constructor() {
  }

  ngOnInit(): void {
    this.eqtldataSource = new MatTableDataSource(this.data);
      this.eqtldataSource.paginator = this.paginator
      this.eqtldataSource.sort = this.sort
    // 其他初始化代码...
  }
  ngOnChanges(changes: SimpleChanges): void {
    if (changes.data && !changes.data.firstChange) {
      this.eqtldataSource = new MatTableDataSource(this.data);
      this.eqtldataSource.paginator = this.paginator
      this.eqtldataSource.sort = this.sort
    }
  }

}
