import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { SharedModule } from 'src/app/shared/shared.module';
import { GroupG4RoutingModule } from './group-g4-routing.module';

import { GroupG4Component } from './group-g4.component';


@NgModule({
  declarations: [GroupG4Component],
  imports: [
    CommonModule,
    GroupG4RoutingModule,
    SharedModule
  ]
})
export class GroupG4Module { }
