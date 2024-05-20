import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { EqtlG4Component } from "./eqtl-g4.component";

const routes: Routes = [{ path: "", component:EqtlG4Component}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class EqtlG4RoutingModule { }
