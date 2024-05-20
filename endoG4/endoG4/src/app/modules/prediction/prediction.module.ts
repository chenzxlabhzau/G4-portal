import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedModule } from 'src/app/shared/shared.module';
import { PredictionRoutingModule } from './prediction-routing.module';

import { PredictionComponent } from './prediction.component';
@NgModule({
  declarations: [PredictionComponent],
  imports: [
    CommonModule,
    PredictionRoutingModule,
    SharedModule
  ]
})
export class PredictionModule { }
