import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { DefaultComponent } from './default.component';

const routes: Routes = [
  {
    path: '',
    component: DefaultComponent,
    children: [
      // dashboard routing
      {
        path: '',
        loadChildren: () => import('src/app/modules/home/home.module').then((m) => m.HomeModule),
      },
      // browse routing
      {
        path: 'predicted-g4',
        loadChildren: () => import('src/app/modules/predicted-g4/predicted-g4.module').then((m) => m.PredictedG4Module),
      },
      {
        path: 'group-g4',
        loadChildren: () => import('src/app/modules/group-g4/group-g4.module').then((m) => m.GroupG4Module)
      },
      {
        path: 'cell-type',
        loadChildren: () => import('src/app/modules/cell-type/cell-type.module').then((m) => m.CellTypeModule)
      },
      {
        path: 'epigenetics',
        loadChildren: () => import('src/app/modules/epigenetics/epigenetics.module').then((m) => m.EpigeneticsModule)
      },
      {
        path: 'epigenetics-g4',
        loadChildren: () => import('src/app/modules/epigenetics-g4/epigenetics-g4.module').then((m) => m.EpigeneticsG4Module)
      },
      {
        path: 'tf-g4',
        loadChildren: () => import('src/app/modules/tf-g4/tf-g4.module').then((m) => m.TfG4Module)
      },
      {
        path: 'eqtl-g4',
        loadChildren: () => import('src/app/modules/eqtl-g4/eqtl-g4.module').then((m) => m.EqtlG4Module)
      },
      {
        path: 'download',
        loadChildren: () => import('src/app/modules/download/download.module').then((m) => m.DownloadModule)
      },
      {
        path: 'help',
        loadChildren: () => import('src/app/modules/help/help.module').then((m) => m.HelpModule)
      },
      {
        path: 'prediction',
        loadChildren: () => import('src/app/modules/prediction/prediction.module').then((m) => m.PredictionModule)
      },
      {
        path: 'detail',
        loadChildren: () => import('src/app/modules/detail/detail.module').then((m) => m.DetailModule)
      },
    ],
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class DefaultRoutingModule {}
