import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import {PredictedG4Component} from "./predicted-g4.component";

const routes: Routes = [{ path: "", component:PredictedG4Component}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class PredictedG4RoutingModule { }
