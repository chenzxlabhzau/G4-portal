import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BaseHttpService } from 'src/app/shared/base-http.service';
import { Observable } from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class TfG4ApiService extends BaseHttpService {

  constructor(http: HttpClient) { super(http)}
  public TFRecords(e:string,sortcol:string,sortOrder:string, pageIndex = 0, pageSize = 10): Observable<any> {
    return this.getData('tf', {
      query: e,
      sortcol: sortcol,
      sort: sortOrder,
      page: pageIndex.toString(),
      size: pageSize.toString(),
    });
  }
  public downloadeTFRecords(e:string): Observable<any> {
    return this.getData('tf/download', {
      query: e
    });
  }
}
