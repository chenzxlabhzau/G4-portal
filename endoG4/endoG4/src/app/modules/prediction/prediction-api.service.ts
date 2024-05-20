import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BaseHttpService } from 'src/app/shared/base-http.service';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PredictionApiService extends BaseHttpService {
  constructor(http: HttpClient) { super(http)}
    public pRecords(seq_str:string,overlapping:string, max_length:number,
                    min_score:number,max_bulge:number,
                    max_mismatch, max_defect,
                    min_loop,max_loop,min_run,max_run): Observable<any> {
    return this.getData('prediction/txtsearch', {
      seq_str:seq_str,
      overlapping: overlapping,
      max_length:max_length,
      min_score: min_score,
      max_bulge: max_bulge,
      max_mismatch: max_mismatch,
      max_defect: max_defect,
      min_loop: min_loop,
      max_loop: max_loop,
      min_run: min_run,
      max_run: max_run,
    });
  }
}
