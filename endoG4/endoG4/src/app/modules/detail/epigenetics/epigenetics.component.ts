import {Component, OnInit, QueryList, ViewChildren} from '@angular/core';
import { ChromatinComponent } from "./chromatin/chromatin.component"
import { DhsComponent } from "./dhs/dhs.component"
import { EnhancerComponent } from "./enhancer/enhancer.component"


@Component({
  selector: 'app-epigenetics',
  templateUrl: './epigenetics.component.html',
  styleUrls: ['./epigenetics.component.css']
})
export class EpigeneticsComponent implements OnInit {
  tabIndex = 0
  @ViewChildren("chromatin") chromatin: QueryList<ChromatinComponent>;
  @ViewChildren("dhs") dhs: QueryList<DhsComponent>;
  @ViewChildren("enhancer") enhancer: QueryList<EnhancerComponent>;

  constructor() {

  }

  ngOnInit(): void {

  }
  exportTable() {
    // 获取当前选中的表格组件
    switch (this.tabIndex) {
      case 0:
        const chromatin: ChromatinComponent = this.chromatin.toArray()[0];
        chromatin.exporter.exportTable("csv")
        break
      case 1:
        const dhs: DhsComponent = this.dhs.toArray()[0];
        dhs.exporter.exportTable("csv")
        break
      case 2:
        const enhancer: EnhancerComponent = this.enhancer.toArray()[0];
        enhancer.exporter.exportTable("csv")
        break
    }
  }


}
