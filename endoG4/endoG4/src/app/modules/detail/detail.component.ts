import {Component, OnInit, ViewChild} from '@angular/core';
import {DetailApiService} from "./detail-api.service";
import { ActivatedRoute } from '@angular/router';
import {Basicrecord} from "../../shared/model/basic";
import {MatPaginator} from '@angular/material/paginator';
import {MatTableDataSource} from '@angular/material/table';
import {MatSort, Sort} from '@angular/material/sort';

@Component({
  selector: 'app-detail',
  templateUrl: './detail.component.html',
  styleUrls: ['./detail.component.css']
})
export class DetailComponent implements OnInit {
  g_id:string;
  G4info:Basicrecord
  tfRecord
  pathwayRecord
  SampleData
  snp_number:number
  dataSource
  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;
  constructor(private route: ActivatedRoute, private DataApiService: DetailApiService) {
  }

  ngOnInit(): void {
    this.route.params.subscribe((params) => {
      this.g_id = params.g_id;
      this.DataApiService.findG4BasicInfo(params.g_id).subscribe((res) => {
        this.G4info = res.basic
        this.snp_number = this.G4info.eqtl_cancer_number + this.G4info.eqtl_gtex_number + this.G4info.eqtl_gwas_number
        this.SampleData = res.de_samples

    });
      this.DataApiService.findG4TF(params.g_id).subscribe((res) => {
        this.tfRecord = res.tf
        this.pathwayRecord = res.pathway
    });
  });
  }
}
