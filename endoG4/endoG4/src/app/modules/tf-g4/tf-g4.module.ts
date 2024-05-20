import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedModule } from 'src/app/shared/shared.module';
import { TfG4RoutingModule } from './tf-g4-routing.module';

import { TfG4Component } from './tf-g4.component';


@NgModule({
  declarations: [TfG4Component],
  imports: [
    CommonModule,
    TfG4RoutingModule,
    SharedModule
  ]
})
export class TfG4Module { }
