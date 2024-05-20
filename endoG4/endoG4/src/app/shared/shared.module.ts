import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { GeneUrl } from './pipes/GeneUrl';
import { MaterialModule } from './material.module';
import { RouterModule } from '@angular/router';
import { HeaderComponent } from './components/header/header.component';
import { FooterComponent } from './components/footer/footer.component';
import { SafeHtml } from './pipes/SVGTrans';
import { G4Seq } from './pipes/G4Seq';
import { GID } from './pipes/GID';
import { HighchartsChartModule } from 'highcharts-angular';


@NgModule({
  declarations: [
    HeaderComponent,SafeHtml,FooterComponent,GeneUrl,G4Seq, GID
  ],
  imports: [
    CommonModule,
    MaterialModule,
    RouterModule,
    FormsModule,
    ReactiveFormsModule,
    HighchartsChartModule
  ],
  exports: [
    MaterialModule,
    FormsModule,
    ReactiveFormsModule,
    HeaderComponent,
    SafeHtml,
    FooterComponent,
    GeneUrl,
    G4Seq, GID
  ],
})
export class SharedModule {}
