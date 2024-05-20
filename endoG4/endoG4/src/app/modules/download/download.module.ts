import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { SharedModule } from 'src/app/shared/shared.module';
import { DownloadRoutingModule } from './download-routing.module';

import { DownloadComponent } from './download.component';

@NgModule({
  declarations: [DownloadComponent],
  imports: [
    CommonModule,
    DownloadRoutingModule,
    SharedModule
  ]
})
export class DownloadModule { }
