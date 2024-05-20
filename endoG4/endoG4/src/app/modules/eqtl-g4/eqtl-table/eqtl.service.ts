import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BaseHttpService } from 'src/app/shared/base-http.service';
import { Observable } from 'rxjs';
import { EqtlRecord } from "../../../shared/model/eqtl-record";

@Injectable({
  providedIn: 'root'
})
export class EqtlService extends BaseHttpService   {

  constructor(http: HttpClient) { super(http);  }
  public eqtlRecords(e:string, eqtlType:string,sortcol:string,sortOrder:string, pageIndex = 0, pageSize = 10): Observable<any> {
    return this.getData('eqtl', {
      query: e,
      eqtlType:eqtlType,
      sortcol: sortcol,
      sort: sortOrder,
      page: pageIndex.toString(),
      size: pageSize.toString(),
    });
  }
    public downloadeqtlRecords(e:string, tabIndex:number): Observable<any> {
    return this.getData('eqtl/download', {
      query: e,
      tabIndex:tabIndex
    });
  }
}
