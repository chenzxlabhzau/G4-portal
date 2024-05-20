import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BaseHttpService } from 'src/app/shared/base-http.service';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class EpiApiService extends BaseHttpService {
  constructor(http: HttpClient) { super(http); }
  public chromRecords(sample:string, query:string, sortcol:string,sortOrder:string, pageIndex = 0, pageSize = 10): Observable<any> {
    return this.getData('epigenetics/chromhmm', {
      sample:sample,
      query:query,
      sortcol:sortcol,
      sort: sortOrder,
      page: pageIndex.toString(),
      size: pageSize.toString(),
    });
  }
  public dhsRecords(sample:string, query:string, sortcol:string,sortOrder:string, pageIndex = 0, pageSize = 10): Observable<any> {
    return this.getData('epigenetics/dhs', {
      sample:sample,
      query:query,
      sortcol:sortcol,
      sort: sortOrder,
      page: pageIndex.toString(),
      size: pageSize.toString(),
    });
  }
  public enhancerRecords(sample:string, query:string, sortcol:string,sortOrder:string, pageIndex = 0, pageSize = 10): Observable<any> {
    return this.getData('epigenetics/h3k27ac', {
      sample:sample,
      query:query,
      sortcol:sortcol,
      sort: sortOrder,
      page: pageIndex.toString(),
      size: pageSize.toString(),
    });
  }
  public downloadepiRecords(tabIndex:number,e:string, sample:string): Observable<any> {
    return this.getData('epigenetics/download', {
      tabIndex:tabIndex,
      query: e,
      sample:sample
    });
  }
  public findSample(eid:string):Observable<any> {
    return this.getData('epigenetics/findSample', {
      eid:eid
    });
  }
}
