import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BaseHttpService } from 'src/app/shared/base-http.service';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class EpigeneticsService extends BaseHttpService{
  constructor(http: HttpClient) { super(http)}
  public SampleRecords(e:string,sortcol:string,sortOrder:string, pageIndex = 0, pageSize = 10): Observable<any> {
    return this.getData('epigenetics/sample', {
      query: e,
      sortcol: sortcol,
      sort: sortOrder,
      page: pageIndex.toString(),
      size: pageSize.toString(),
    });
  }


  public downloadSampleRecords(e:string): Observable<any> {
    return this.getData('epigenetics/sample_donwload', {
      query: e
    });
  }
}
