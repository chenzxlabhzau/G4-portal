import { Component, OnInit, AfterViewInit, ViewChild } from '@angular/core';
import {  tap } from 'rxjs/operators';
import { merge } from 'rxjs';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { FormControl } from '@angular/forms';
import { environment } from '../../../environments/environment';
import { PredictedG4ApiService } from './predicted-g4-api.service';
import { pG4DataSource } from './predicted-g4-source';

@Component({
  selector: 'app-predicted-g4',
  templateUrl: './predicted-g4.component.html',
  styleUrls: ['./predicted-g4.component.css']
})
export class PredictedG4Component implements OnInit, AfterViewInit {
  assets = environment.assets;
  @ViewChild(MatPaginator) paginator: MatPaginator | undefined;
  @ViewChild(MatSort) sort: MatSort | undefined;
  dataSource: pG4DataSource | undefined;
  downloading = false
  displayedColumns = ["g_id",'loci','score','sample_number','gene_id',"gene_name","gene_type","phastCons","phyloP","seq"];
  // displayedColumns = ['loci', 'score','gene_id',"gene_name","gene_type"];
  Species:string[] = ["Human","Mouse","Pig","Chicken", "Rhesus macaque","Rat",
    "Rabbit", "Opossums", "Zebrafish", "Fruit fly", "C. elegans"]
  species:string = "Human";
  genome:string = "hg19"
  trackFile:string = "endoG4_hg19_track_info.txt"
  isLegalInput = true;
  hasRequest = false;
  searchFormControl = new FormControl();
  constructor(private DataApiService: PredictedG4ApiService) {
    this.dataSource = new pG4DataSource(this.DataApiService);
  }

  ngOnInit(): void {
    this.searchFormControl.valueChanges.pipe(tap((val) => {
    // http is requesting, isLoading true
    this.isLegalInput = this._checkInput(val);
    this.hasRequest = false;
  })).subscribe()
    this.dataSource.loadpG4Records("","Human",undefined,"",0,10)
  }

  ngAfterViewInit(): void {
    this.paginator.page.pipe(tap(() => this.update()));
    this.sort.sortChange.subscribe(() => (this.paginator.pageIndex = 0));
     merge(this.sort.sortChange, this.paginator.page)
        .pipe(tap(() => this.update()))
        .subscribe();
  }

  public search(): void {
    switch (this.species){
      case "Human":
        this.genome = "hg19";
        this.trackFile = "endoG4_hg19_track_info.txt"
        break;
      case "Mouse":
        this.genome = "mm10";
        this.trackFile = "endoG4_mm10_track_info.txt";
        break;
      case "Pig":
        this.genome = "susScr11";
        this.trackFile = "endoG4_susScr11_track_info.txt";
        break;
      case "Chicken":
        this.genome = "galGal6";
        this.trackFile = "endoG4_galGal6_track_info.txt";
        break;
      case "Rhesus macaque":
        this.genome = "rheMac10";
        this.trackFile = "endoG4_rheMac10_track_info.txt";
        break;
      case "Rat":
        this.genome = "rn7";
        this.trackFile = "endoG4_rn7_track_info.txt";
        break;
      case "Rabbit":
        this.genome = "oryCun2";
        this.trackFile = "endoG4_oryCun2_track_info.txt";
        break;
      case "Opossums":
        this.genome = "monDom5";
        this.trackFile = "endoG4_monDom5_track_info.txt";
        break;
      case "Zebrafish":
        this.genome = "danRer11";
        this.trackFile = "endoG4_danRer11_track_info.txt";
        break;
      case "Fruit fly":
        this.genome = "dm6";
        this.trackFile = "endoG4_dm6_track_info.txt";
        break;
      case "C. elegans":
        this.genome = "ce11";
        this.trackFile = "endoG4_ce11_track_info.txt";
        break;
    }
    console.log(this.genome)
    this.paginator.pageIndex = 0
    this.dataSource.loadpG4Records(
      this.searchFormControl.value,
      this.species,
      this.sort.active,
      this.sort.direction,
      this.paginator.pageIndex,
      this.paginator.pageSize
    );
    if (["Human","Mouse","Pig"].includes(this.species)){
      this.displayedColumns = ["g_id",'loci','score','sample_number','gene_id',"gene_name","gene_type","phastCons","phyloP","seq"];
    }else if(["Chicken","Fruit fly", "C. elegans"].includes(this.species)){
      this.displayedColumns = ["g_id",'loci','score','gene_id',"gene_name","gene_type","phastCons","phyloP","seq"];
    }else {
      this.displayedColumns = ["g_id",'loci','score','gene_id',"gene_name","gene_type","seq"];
    }
  }
  public update(): void {
    this.dataSource.loadpG4Records(
      this.searchFormControl.value,
      this.species,
      this.sort.active,
      this.sort.direction,
      this.paginator.pageIndex,
      this.paginator.pageSize
    );
  }
  public download(): void {
    this.downloading = true
    this.DataApiService.downloadpG4Records(
      this.searchFormControl.value,
      this.species
    ).pipe(tap((val) => {
      this.downloading = false
      this.DataApiService.downloadFile(environment.Burl+"/static/download/predicted/" + val.replace(/"/g,"")
      ,"Predicted-G4_result.csv")
      console.log(val)
    })).subscribe();
  }
  private _checkInput(s: string): boolean {
    const regex = /[!@#$%^&*()\=\[\]{};'"\\|<>\/?]/g;
    return !regex.test(s);
  }
}
