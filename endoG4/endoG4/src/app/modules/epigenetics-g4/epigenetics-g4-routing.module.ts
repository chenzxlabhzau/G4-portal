import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {EpigeneticsG4Component} from "./epigenetics-g4.component";

const routes: Routes = [{ path: ":sample_id", component:EpigeneticsG4Component}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class EpigeneticsG4RoutingModule { }
