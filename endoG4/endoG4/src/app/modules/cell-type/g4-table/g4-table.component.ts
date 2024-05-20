import { Component, OnInit, Input, AfterViewInit, ViewChild, SimpleChanges, OnChanges } from '@angular/core';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { G4TableDatasource } from './g4-table-datasource'
import {CellTypeService} from '../cell-type.service'
import {tap} from "rxjs/operators";
import {merge} from "rxjs";


@Component({
  selector: 'app-g4-table',
  templateUrl: './g4-table.component.html',
  styleUrls: ['./g4-table.component.css']
})
export class G4TableComponent implements OnInit, OnChanges, AfterViewInit {
  @Input() sl_sample: string;
  @Input() query: string;

  @ViewChild(MatPaginator) paginator: MatPaginator | undefined;
  @ViewChild(MatSort) sort: MatSort | undefined;
  dataSource: G4TableDatasource | undefined;
  displayedColumns = ['g_id','loci', 'group', 'sample' ,'cell_line','treat','type','source'];
  constructor(private cellTypeService:CellTypeService) {
    this.dataSource = new G4TableDatasource(this.cellTypeService);
    this.dataSource.loadG4SampleRecords("","",undefined,"",0,10)
  }
  ngOnChanges(changes: SimpleChanges): void {
    console.log("ok")
    if (!(Object.values(changes)[0].firstChange )){
      this.paginator.pageIndex = 0
      this._loadsampleRecordsPage()
    }
    }
  ngOnInit(): void {

  }
  ngAfterViewInit(): void {
    this.paginator.page.pipe(tap(() => this._loadsampleRecordsPage()));
    this.sort.sortChange.subscribe(() => (this.paginator.pageIndex = 0));
     merge(this.sort.sortChange, this.paginator.page)
        .pipe(tap(() => this._loadsampleRecordsPage()))
        .subscribe();
  }

  private _loadsampleRecordsPage(): void {
    console.log(this.sl_sample)
    this.dataSource.loadG4SampleRecords(
      this.sl_sample,
      this.query,
      this.sort.active,
      this.sort.direction,
      this.paginator.pageIndex,
      this.paginator.pageSize
    );
  }
}
