import { Component, OnInit } from '@angular/core';
import {environment} from "../../../environments/environment";
import all_samples from "../../shared/constants/samples";
import {tap} from "rxjs/operators";
import {CellTypeService} from "./cell-type.service";
import {FormControl} from "@angular/forms";

@Component({
  selector: 'app-cell-type',
  templateUrl: './cell-type.component.html',
  styleUrls: ['./cell-type.component.css']
})
export class CellTypeComponent implements OnInit {
  assets = environment.assets;
  sample:string
  samples: string[] = all_samples
  sl_sample:string
  downloading = false
  query:string = ""
  searchFormControl = new FormControl();
  constructor(private DataApiService: CellTypeService) { }

  ngOnInit(): void {
  }

  public search(): void {
    console.log(this.sample)
    this.sl_sample = this.sample
    this.query = this.searchFormControl.value
  }
  public download(): void {
    this.downloading = true
    this.DataApiService.downloadsampleRecords(
      this.query,
      this.sample
    ).pipe(tap((val) => {
      this.downloading = false
      this.DataApiService.downloadFile(environment.Burl+"/static/download/celltype/" + val.replace(/"/g,""),
        "eG4_celltype_result.csv")
      console.log(val)
    })).subscribe();
  }
  public sampleselect($event: any){
    this.sample=$event
    this.sl_sample=$event
    this.searchFormControl.setValue("")
    this.query=""
  }
}
