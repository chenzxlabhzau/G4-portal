import { Component, OnInit, Input, AfterViewInit, ViewChild, SimpleChanges, OnChanges } from '@angular/core';
import { tap } from 'rxjs/operators';
import { merge } from 'rxjs';
import { EpiApiService } from '../epi-api.service';
import { dhsDataSource } from './dhs-data-source';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';

@Component({
  selector: 'app-dhs',
  templateUrl: './dhs.component.html',
  styleUrls: ['./dhs.component.css']
})
export class DhsComponent implements OnInit, OnChanges, AfterViewInit {
  @Input() sl_sample: string;
  @Input() query: string;
  @ViewChild(MatPaginator) paginator: MatPaginator | undefined;
  @ViewChild(MatSort) sort: MatSort | undefined;
  dataSource: dhsDataSource | undefined;

  displayedColumns = ['g_id','loci', 'group', 'gene_id' ,'gene_name','gene_type','epi_loci','peak_score'];

  constructor(private DataApiService: EpiApiService) {
    this.dataSource = new dhsDataSource(this.DataApiService);
  }

  ngOnInit(): void {
    // this.dataSource = new sampleDataSource(this.DataApiService);
    this.dataSource.loaddhsRecords("E003", "", undefined, "", 0, 10);
    console.log(this.sl_sample)
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (!(Object.values(changes)[0].firstChange)) {
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
    this.dataSource.loaddhsRecords(
      this.sl_sample,
      this.query,
      this.sort.active,
      this.sort.direction,
      this.paginator.pageIndex,
      this.paginator.pageSize
    );
  }
}
