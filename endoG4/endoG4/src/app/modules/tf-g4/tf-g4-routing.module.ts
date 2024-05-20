import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {TfG4Component} from "./tf-g4.component";

const routes: Routes = [{ path: "", component:TfG4Component}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class TfG4RoutingModule { }
