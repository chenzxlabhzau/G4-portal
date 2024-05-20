import { Component, OnInit } from '@angular/core';
import {FormControl} from "@angular/forms";
import {EqtlService} from "./eqtl-table/eqtl.service";
import {tap} from "rxjs/operators";
import {environment} from "../../../environments/environment";


@Component({
  selector: 'app-eqtl-g4',
  templateUrl: './eqtl-g4.component.html',
  styleUrls: ['./eqtl-g4.component.css']
})
export class EqtlG4Component implements OnInit {
  assets = environment.assets;
  query:string
  tabIndex = 0
  downloading = false
  eqtlTypes=[
    {"show":"GWAS SNP","label":"eqtl_gwas"},
    {"show":"GTEX eQTL","label":"eqtl_gtex"},
    {"show":"Cancer eQTL","label":"eqtl_cancer"}
  ]
  isLegalInput = true;
  searchFormControl = new FormControl();
  constructor(private DataApiService: EqtlService) { }

  ngOnInit(): void {
  }
  public search(): void {
    if (this.searchFormControl.value.indexOf(":")!=-1 && this.searchFormControl.value.startsWith("chr")){
      if (this.searchFormControl.value.indexOf("-")==-1){
        alert("If you want to retrieve a region, enter it according to the specification (ex. chr1:10000-100000)")
      return
      }
    }
    console.log(this.searchFormControl.value)
    this.query = this.searchFormControl.value
  }
  public download(): void {
    this.downloading = true
    console.log("download")
    this.DataApiService.downloadeqtlRecords(
      this.searchFormControl.value,
      this.tabIndex
    ).pipe(tap((val) => {
      this.downloading = false
      this.DataApiService.downloadFile(environment.Burl+"/static/download/eqtl/" + val.replace(/"/g,""),
        "eG4_eQTL_result.csv")
      console.log(val)
    })).subscribe();
  }
}
