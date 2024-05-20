import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {EpigeneticsComponent} from "./epigenetics.component";

const routes: Routes = [{ path: "", component:EpigeneticsComponent}];
@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class EpigeneticsRoutingModule { }
