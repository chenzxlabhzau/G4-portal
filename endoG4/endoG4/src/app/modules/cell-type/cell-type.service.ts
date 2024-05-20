import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BaseHttpService } from 'src/app/shared/base-http.service';
import { Observable } from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class CellTypeService extends BaseHttpService{
  constructor(http: HttpClient) { super(http)}

  public SampleRecords(s:string, q:string,sortcol:string,sortOrder:string, pageIndex = 0, pageSize = 10): Observable<any> {
    return this.getData('celltype/sample', {
      sample:s,
      query: q,
      sortcol: sortcol,
      sort: sortOrder,
      page: pageIndex.toString(),
      size: pageSize.toString(),
    });
  }
  public downloadsampleRecords(q:string, sample:string): Observable<any> {
    return this.getData('celltype/download', {
      query: q,
      sample:sample
    });
  }
  public SampleInfo(): Observable<any> {
    return this.getData('celltype/sample_info');
  }
}
