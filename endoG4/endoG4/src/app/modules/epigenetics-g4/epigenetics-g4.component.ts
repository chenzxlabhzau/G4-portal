import { Component, OnInit } from '@angular/core';
import {FormControl} from "@angular/forms";
import {tap} from "rxjs/operators";
import authors from 'src/app/shared/constants/authors';
import { environment } from '../../../environments/environment';
import { EpiApiService } from './epi-api.service';
import {ActivatedRoute} from "@angular/router";


@Component({
  selector: 'app-epigenetics-g4',
  templateUrl: './epigenetics-g4.component.html',
  styleUrls: ['./epigenetics-g4.component.css']
})
export class EpigeneticsG4Component implements OnInit {
  assets = environment.assets;
  tabIndex = 0
  samples: string[] = authors
  sample: string
  sl_sample:string
  downloading = false
  query:string
  isLegalInput = true;
  sample_info = undefined
  searchFormControl = new FormControl();
  constructor(private route: ActivatedRoute, private DataApiService: EpiApiService) {
    this.route.params.subscribe((params) => {
      this.sample = params.sample_id;
      this.sl_sample = params.sample_id;
      this.DataApiService.findSample(params.sample_id).subscribe((res) => {
        this.sample_info = res
    });
      console.log(this.sample_info)
    })
  }
  onSelectionChange(event) {
      this.DataApiService.findSample(this.sample).subscribe((res) => {
        this.sample_info = res
    });
    // handle selection change event here
  }
  ngOnInit(): void {
    this.searchFormControl.valueChanges.pipe(tap((val) => {
    this.isLegalInput = this._checkInput(val);
  })).subscribe()
  }
  public search(): void {
    console.log(this.sample)
    this.sl_sample = this.sample
    this.query = this.searchFormControl.value
  }
  public download(): void {
    this.downloading = true
    this.DataApiService.downloadepiRecords(
      this.tabIndex,
      this.searchFormControl.value,
      this.sample
    ).pipe(tap((val) => {
      this.downloading = false
      this.DataApiService.downloadFile(environment.Burl+"/static/download/epigenetics/" + val.replace(/"/g,""),
        "eG4_epigenetic_result.csv")
      console.log(val)
    })).subscribe();
  }
  private _checkInput(s: string): boolean {
    const regex = /[!@#$%^&*()\=\[\]{};'"\\|<>\/?]/g;
    return !regex.test(s);
  }
}
