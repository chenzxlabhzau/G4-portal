import { Component, OnInit, Input, AfterViewInit, ViewChild, SimpleChanges, OnChanges } from '@angular/core';
import {  tap } from 'rxjs/operators';
import { merge, fromEvent } from 'rxjs';
import { EpiApiService } from '../epi-api.service';
import { chromhmmDataSource } from './chromhmm-data-source';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';


@Component({
  selector: 'app-chrom-hmm',
  templateUrl: './chrom-hmm.component.html',
  styleUrls: ['./chrom-hmm.component.css']
})
export class ChromHMMComponent implements OnInit ,OnChanges, AfterViewInit {
  @Input() sl_sample:string;
  @Input() query:string;
  @ViewChild(MatPaginator) paginator: MatPaginator | undefined;
  @ViewChild(MatSort) sort: MatSort | undefined;
  dataSource: chromhmmDataSource | undefined;

  displayedColumns = ['g_id','loci', 'group', 'gene_id' ,'gene_name','gene_type','epi_loci','state'];
  constructor(private DataApiService: EpiApiService) {
    this.dataSource = new chromhmmDataSource(this.DataApiService);
  }

  ngOnInit(): void {
    // this.dataSource = new sampleDataSource(this.DataApiService);
    this.dataSource.loadchromhmmRecords("E003", "",undefined,"", 0, 10);
  }
  ngOnChanges(changes: SimpleChanges): void {
    if (!(Object.values(changes)[0].firstChange )){
      this.paginator.pageIndex = 0
      this._loadRecordsPage()
    }
  }
  ngAfterViewInit():void {
    this.paginator.page.pipe(tap(() => this._loadRecordsPage()));
    this.sort.sortChange.subscribe(() => (this.paginator.pageIndex = 0));
     merge(this.sort.sortChange, this.paginator.page)
        .pipe(tap(() => this._loadRecordsPage()))
        .subscribe();
  }

  private _loadRecordsPage(): void {
    this.dataSource.loadchromhmmRecords(
      this.sl_sample,
      this.query,
      this.sort.active,
      this.sort.direction,
      this.paginator.pageIndex,
      this.paginator.pageSize
    );
  }
}
