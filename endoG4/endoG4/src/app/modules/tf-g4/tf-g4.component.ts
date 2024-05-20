import {AfterViewInit, Component, OnInit, ViewChild} from '@angular/core';
import {  tap } from 'rxjs/operators';
import { merge } from 'rxjs';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { FormControl } from '@angular/forms';
import {environment} from "../../../environments/environment";

import { TfG4ApiService } from './tf-g4-api.service';
import { TFDataSource } from './tf-g4-source';
@Component({
  selector: 'app-tf-g4',
  templateUrl: './tf-g4.component.html',
  styleUrls: ['./tf-g4.component.css']
})
export class TfG4Component implements OnInit, AfterViewInit {
  assets = environment.assets;
  @ViewChild(MatPaginator) paginator: MatPaginator | undefined;
  @ViewChild(MatSort) sort: MatSort | undefined;
  dataSource: TFDataSource | undefined;
  displayedColumns = ['g_id','loci','tf', 'tfloci', 'score','match_seq'];
  isLegalInput = true;
  hasRequest = false;
  searchFormControl = new FormControl();
  downloading = false
  constructor(private DataApiService: TfG4ApiService) {
    this.dataSource = new TFDataSource(this.DataApiService);
  }

  ngOnInit(): void {
    this.searchFormControl.valueChanges.pipe(tap((val) => {
      this.paginator.pageIndex = 0
    // http is requesting, isLoading true
      this.isLegalInput = this._checkInput(val);
      this.hasRequest = false;
  })).subscribe()
    this.dataSource.loadTFRecords("",undefined,"",0,10)
  }
  ngAfterViewInit(): void {
    this.paginator.page.pipe(tap(() => this.search()));
    this.sort.sortChange.subscribe(() => (this.paginator.pageIndex = 0));
     merge(this.sort.sortChange, this.paginator.page)
        .pipe(tap(() => this.search()))
        .subscribe();
  }
  public search(): void {
    this.dataSource.loadTFRecords(
      this.searchFormControl.value,
      this.sort.active,
      this.sort.direction,
      this.paginator.pageIndex,
      this.paginator.pageSize
    );
  }

  public download(): void {
    this.downloading = true
    console.log("download")
    this.DataApiService.downloadeTFRecords(
      this.searchFormControl.value,
    ).pipe(tap((val) => {
      this.downloading = false
      this.DataApiService.downloadFile(environment.Burl+"/static/download/TF/" + val.replace(/"/g,""),
        "eG4_TF_result.csv")
      console.log(val)
    })).subscribe();
  }
  private _checkInput(s: string): boolean {
    const regex = /[!@#$%^&*()_\=\[\]{};'"\\|<>\/?]/g;
    return !regex.test(s);
  }

}
