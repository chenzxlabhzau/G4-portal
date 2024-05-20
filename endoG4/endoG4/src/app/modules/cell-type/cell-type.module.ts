import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { CellTypeRoutingModule } from './cell-type-routing.module';
import { G4TableComponent } from './g4-table/g4-table.component';
import { SampleTableComponent } from './sample-table/sample-table.component';
import { CellTypeComponent } from './cell-type.component';
import { SharedModule } from 'src/app/shared/shared.module';

@NgModule({
  declarations: [
    CellTypeComponent,
    G4TableComponent,
    SampleTableComponent
  ],
  imports: [
    CommonModule,
    CellTypeRoutingModule,
    SharedModule
  ]
})
export class CellTypeModule { }
