import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { SharedModule } from 'src/app/shared/shared.module';
import { PredictedG4RoutingModule } from './predicted-g4-routing.module';

import { PredictedG4Component } from './predicted-g4.component';

@NgModule({
  declarations: [PredictedG4Component],
  imports: [
    CommonModule,
    PredictedG4RoutingModule,
    SharedModule
  ]
})
export class PredictedG4Module { }
