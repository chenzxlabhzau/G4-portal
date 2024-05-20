import {AfterViewInit, Component, OnInit, ViewChild} from '@angular/core';
import {MatPaginator} from "@angular/material/paginator";
import {MatSort} from "@angular/material/sort";
import {eG4DataSource} from "./group-g4-source";
import {FormControl} from "@angular/forms";
import {GroupG4ApiService} from "./group-g4-api.service";
import {tap} from "rxjs/operators";
import {merge} from "rxjs";
import {environment} from "../../../environments/environment";

@Component({
  selector: 'app-group-g4',
  templateUrl: './group-g4.component.html',
  styleUrls: ['./group-g4.component.css']
})
export class GroupG4Component implements OnInit, AfterViewInit {
  assets = environment.assets;
  @ViewChild(MatPaginator) paginator: MatPaginator | undefined;
  @ViewChild(MatSort) sort: MatSort | undefined;
  dataSource: eG4DataSource | undefined;
  downloading = false
  displayedColumns = ["g_id",'loci', "size",'score','sample_number','gene_id',"gene_name","gene_type","phastCons","phyloP","seq"];
  Groups:string[] = ["Level1","Level2","Level3","Level4","Level5","Level6"]
  species:string[] = ["Human","Mouse","Chicken"]
  sp = "Human"
  group:string;
  isLegalInput = true;
  hasRequest = false;
  searchFormControl = new FormControl();
  constructor(private DataApiService: GroupG4ApiService) {
    this.dataSource = new eG4DataSource(this.DataApiService);
  }

  ngOnInit(): void {
    this.searchFormControl.valueChanges.pipe(tap((val) => {
    // http is requesting, isLoading true
    this.isLegalInput = this._checkInput(val);
    this.hasRequest = false;
  })).subscribe()
    this.dataSource.loadpG4Records("","Human",undefined,undefined,"",0,10)
  }

  ngAfterViewInit(): void {
    this.paginator.page.pipe(tap(() => this.update()));
    this.sort.sortChange.subscribe(() => (this.paginator.pageIndex = 0));
     merge(this.sort.sortChange, this.paginator.page)
        .pipe(tap(() => this.update()))
        .subscribe();
  }

  public search(): void {
    if (this.searchFormControl.value.indexOf(":")!=-1 && this.searchFormControl.value.startsWith("chr")){
      if (this.searchFormControl.value.indexOf("-")==-1){
        alert("If you want to retrieve a region, enter it according to the specification (ex. chr1:10000-100000)")
      return
      }
    }
    // 需要写一个检查坐标是否为region的方法
    this.paginator.pageIndex = 0
    this.dataSource.loadpG4Records(
      this.searchFormControl.value,
      this.sp,
      this.group,
      this.sort.active,
      this.sort.direction,
      this.paginator.pageIndex,
      this.paginator.pageSize
    );
  }
  private update(): void {
    this.dataSource.loadpG4Records(
      this.searchFormControl.value,
      this.sp,
      this.group,
      this.sort.active,
      this.sort.direction,
      this.paginator.pageIndex,
      this.paginator.pageSize
    );
  }
  public download(): void {
    this.downloading = true
    console.log("download")
    this.DataApiService.downloadeG4Records(
      this.searchFormControl.value,
      this.sp,
      this.group
    ).pipe(tap((val) => {
      this.downloading = false
      this.DataApiService.downloadFile(environment.Burl+"/static/download/group/" + val.replace(/"/g,""),
        "eG4_result.csv")
      console.log(val)
    })).subscribe();
  }

  private _checkInput(s: string): boolean {
    const regex = /[!@#$%^&*()\=\[\]{};'"\\|<>\/?]/g;
    return !regex.test(s);
  }

}
