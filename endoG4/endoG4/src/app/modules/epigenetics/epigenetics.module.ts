import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { EpigeneticsRoutingModule } from './epigenetics-routing.module';
import { SharedModule } from 'src/app/shared/shared.module';


import { EpigeneticsComponent } from './epigenetics.component';

@NgModule({
  declarations: [EpigeneticsComponent],
  imports: [
    CommonModule,
    EpigeneticsRoutingModule,
    SharedModule
  ]
})
export class EpigeneticsModule { }
