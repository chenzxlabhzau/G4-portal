import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { SharedModule } from 'src/app/shared/shared.module';
import { HelpRoutingModule } from './help-routing.module';

import { HelpComponent } from './help.component';
import { VersionComponent } from './version/version.component';
import { StatisticsComponent } from './statistics/statistics.component';

@NgModule({
  declarations: [HelpComponent, VersionComponent, StatisticsComponent],
  imports: [
    CommonModule,
    HelpRoutingModule,
    SharedModule
  ]
})
export class HelpModule { }
