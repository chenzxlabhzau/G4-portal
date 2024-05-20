import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { SharedModule } from 'src/app/shared/shared.module';
import { EpigeneticsG4RoutingModule } from './epigenetics-g4-routing.module';

import { EpigeneticsG4Component } from './epigenetics-g4.component';
import { ChromHMMComponent } from './chrom-hmm/chrom-hmm.component';
import { DhsComponent } from './dhs/dhs.component';
import { EnhancerComponent } from './enhancer/enhancer.component';

@NgModule({
  declarations: [EpigeneticsG4Component, ChromHMMComponent, DhsComponent, EnhancerComponent],
  imports: [
    CommonModule,
    EpigeneticsG4RoutingModule,
    SharedModule
  ]
})
export class EpigeneticsG4Module { }
