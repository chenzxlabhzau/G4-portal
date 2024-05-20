import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {CellTypeComponent} from "./cell-type.component";

const routes: Routes = [{ path: "", component:CellTypeComponent}];
@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class CellTypeRoutingModule { }
