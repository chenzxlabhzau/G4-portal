import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import {GroupG4Component} from "./group-g4.component";

const routes: Routes = [{ path: "", component:GroupG4Component}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class GroupG4RoutingModule { }
