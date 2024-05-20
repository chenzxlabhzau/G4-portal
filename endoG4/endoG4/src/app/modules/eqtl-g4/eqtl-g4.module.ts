import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SharedModule } from 'src/app/shared/shared.module';
import { EqtlG4RoutingModule } from './eqtl-g4-routing.module';

import { EqtlG4Component } from './eqtl-g4.component';
import { EqtlTableComponent } from './eqtl-table/eqtl-table.component';


@NgModule({
  declarations: [EqtlG4Component, EqtlTableComponent],
  imports: [
    CommonModule,
    EqtlG4RoutingModule,
    SharedModule
  ]
})
export class EqtlG4Module { }
