import {Component, OnInit, ViewChild} from '@angular/core';
import {environment} from "../../../environments/environment";
import {MatPaginator} from "@angular/material/paginator";
import {MatSort} from "@angular/material/sort";
import {FormControl} from "@angular/forms";
import {tap} from "rxjs/operators";
import {EpigeneticsService} from "./epigenetics.service";
import {SampleDataSource} from "./epigenetics-source";
import {merge} from "rxjs";



@Component({
  selector: 'app-epigenetics',
  templateUrl: './epigenetics.component.html',
  styleUrls: ['./epigenetics.component.css']
})
export class EpigeneticsComponent implements OnInit {
  assets = environment.assets;
  downloading = false
  @ViewChild(MatPaginator) paginator: MatPaginator | undefined;
  @ViewChild(MatSort) sort: MatSort | undefined;
  dataSource: SampleDataSource| undefined;
  searchFormControl = new FormControl();
  isLegalInput = true;
  displayedColumns = ["Sample_id",'sample_name','Group', "ANATOMY",'TYPE','AGE','SEX',"Under_seq","Quality_rating"];
  constructor(private DataApiService: EpigeneticsService) {
    this.dataSource = new SampleDataSource(this.DataApiService);
    this.dataSource.loadSampleRecords("",undefined,"",0,10)
  }

  ngOnInit(): void {
    this.searchFormControl.valueChanges.pipe(tap((val) => {
    // http is requesting, isLoading true
    this.isLegalInput = this._checkInput(val);
  })).subscribe()

  }
  ngAfterViewInit(): void {
    this.paginator.page.pipe(tap(() => this.update()));
    this.sort.sortChange.subscribe(() => (this.paginator.pageIndex = 0));
     merge(this.sort.sortChange, this.paginator.page)
        .pipe(tap(() => this.update()))
        .subscribe();
  }
  private update(): void {
    this.dataSource.loadSampleRecords(
      this.searchFormControl.value,
      this.sort.active,
      this.sort.direction,
      this.paginator.pageIndex,
      this.paginator.pageSize
    );
  }
  public search(): void {
    this.paginator.pageIndex = 0
    this.update()
  }
  public download(): void {
    this.downloading = true
    console.log("download")
    this.DataApiService.downloadSampleRecords(
      this.searchFormControl.value
    ).pipe(tap((val) => {
      this.downloading = false
      this.downloadFile(environment.Burl+"/static/download/sample/" + val.replace(/"/g,""),
        "sample.txt")
      console.log(environment.Burl+"/static/download/sample/" + val.replace(/"/g,""))
    })).subscribe();
  }

  public downloadFile(filePath,filename){
    var link=document.createElement('a');
    link.href = filePath;
    link.download = filename
    link.click();
  }
  private _checkInput(s: string): boolean {
    const regex = /[!@#$%^&*()_\=\[\]{};'"\\|<>\/?]/g;
    return !regex.test(s);
  }
}
