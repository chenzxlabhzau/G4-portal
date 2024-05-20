import {Component, OnInit, Input, ViewChild, AfterViewInit, SimpleChanges, OnChanges} from '@angular/core';
import { merge } from 'rxjs';
import {  tap } from 'rxjs/operators';
import { ActivatedRoute } from '@angular/router';
import { MatPaginator } from "@angular/material/paginator";
import { MatSort } from "@angular/material/sort";
import { EqtlService } from "./eqtl.service";
import { eqtlDataSource } from "./eqtl-data-source";

@Component({
  selector: 'app-eqtl-table',
  templateUrl: './eqtl-table.component.html',
  styleUrls: ['./eqtl-table.component.css']
})
export class EqtlTableComponent implements OnInit,OnChanges, AfterViewInit{
  @Input() eqtlType:string;
  @Input() query:string;
  @ViewChild(MatPaginator) paginator: MatPaginator | undefined;
  @ViewChild(MatSort) sort: MatSort | undefined;
  dataSource: eqtlDataSource | undefined;
  constructor(private eqtlService: EqtlService) { }
  displayedColumns = ['g_id','loci', 'group',"score",'rsid', 'cloci',"allele",'phenotype',"new_score"];

  ngOnInit(): void {
    if (this.eqtlType=="eqtl_gwas"){
      this.displayedColumns = ['g_id','loci', 'group',"score",'rsid', 'cloci',"allele",'phenotype',"new_score"];
    }else {
      this.displayedColumns = ['g_id','loci', 'group',"score",'rsid', 'cloci',"allele", "gene",'phenotype',"new_score"];
    }
    this.dataSource = new eqtlDataSource(this.eqtlService);
    this.dataSource.loadeqtlRecords(this.query, this.eqtlType, undefined, "", 0, 10);
  }
   ngAfterViewInit(): void {
    merge(this.sort.sortChange, this.paginator.page)
      .pipe(tap(() => this._loadRecordsPage()))
      .subscribe();
   }
  ngOnChanges(changes: SimpleChanges): void {
    if (!(Object.values(changes)[0].firstChange)) {
      this.paginator.pageIndex = 0
      this._loadRecordsPage()
    }
  }
  private _loadRecordsPage(): void {
    this.dataSource.loadeqtlRecords(
      this.query,
      this.eqtlType,
      this.sort.active,
      this.sort.direction,
      this.paginator.pageIndex,
      this.paginator.pageSize
    );
  }
}
