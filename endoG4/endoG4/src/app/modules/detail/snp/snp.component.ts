import {Component, Input, OnInit, ViewChild, ViewChildren, QueryList} from '@angular/core';
import { MatPaginator } from "@angular/material/paginator";
import { MatSort } from "@angular/material/sort";
import {EqtlTableComponent} from "./eqtl-table/eqtl-table.component"
import {ActivatedRoute} from "@angular/router";
import {DetailApiService} from "../detail-api.service";

@Component({
  selector: 'app-snp',
  templateUrl: './snp.component.html',
  styleUrls: ['./snp.component.css']
})
export class SnpComponent implements OnInit {
  g_id: string
  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;
  @Input() eqtl_cancer:number
  @Input() eqtl_gtex:number
  @Input() eqtl_gwas:number
  tabIndex = 0
  eqtlTypes
  data: any[] = [];
  @ViewChildren('eqtlTable') eqtlTables: QueryList<EqtlTableComponent>;
  constructor(private route: ActivatedRoute, private DataApiService: DetailApiService) {
    this.route.params.subscribe((params) => {
      this.g_id = params.g_id;
  });
  }
  exportTable() {
    // 获取当前选中的表格组件
    const eqtlTable: EqtlTableComponent = this.eqtlTables.toArray()[this.tabIndex];
    console.log(eqtlTable)
    console.log(this.eqtlTables)
    // 导出当前选中的表格
  // 保护措施：如果eqtlTable或者其exportTable方法不存在，不执行后续代码
    if (eqtlTable && eqtlTable.exportTable) {
      eqtlTable.exportTable();
    } else {
    }
  }
  ngOnInit(): void {
    this.eqtlTypes=[
      {"show":"GWAS SNP","label":"eqtl_gwas", "number": this.eqtl_gwas},
      {"show":"GTEX eQTL","label":"eqtl_gtex", "number": this.eqtl_gtex},
      {"show":"Cancer eQTL","label":"eqtl_cancer", "number": this.eqtl_gwas}
    ]
    this.eqtlTypes.sort((a, b) => b.number - a.number)
    for (let i = 0; i < this.eqtlTypes.length; i++) {
      this.DataApiService.findG4SNP(this.g_id, this.eqtlTypes[i].label).subscribe((res) => {
        this.data[i] = res;
      });
    }

  }

}
