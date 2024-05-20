import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { DetailRoutingModule } from './detail-routing.module';
import { SharedModule } from 'src/app/shared/shared.module';
import { DetailComponent } from './detail.component';
import { BasicComponent } from './basic/basic.component';
import { EpigeneticsComponent } from './epigenetics/epigenetics.component';
import { TfComponent } from './tf/tf.component';
import { SnpComponent } from './snp/snp.component';
import { ChromatinComponent } from './epigenetics/chromatin/chromatin.component';
import { DhsComponent } from './epigenetics/dhs/dhs.component';
import { EnhancerComponent } from './epigenetics/enhancer/enhancer.component';
import { EqtlTableComponent } from './snp/eqtl-table/eqtl-table.component';
import { PathwayComponent } from './pathway/pathway.component';
import { MatTableExporterModule } from 'mat-table-exporter';
import { SampleComponent } from './sample/sample.component';
import { EnrichmentComponent } from './enrichment/enrichment.component';
import { HighchartsChartModule } from 'highcharts-angular';

@NgModule({
  declarations: [DetailComponent, BasicComponent, EpigeneticsComponent, TfComponent, SnpComponent, ChromatinComponent, DhsComponent, EnhancerComponent, EqtlTableComponent, PathwayComponent, SampleComponent, EnrichmentComponent],
  imports: [
    CommonModule,
    DetailRoutingModule,
    SharedModule,
    MatTableExporterModule,
    HighchartsChartModule
  ]
})
export class DetailModule { }
