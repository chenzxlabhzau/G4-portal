import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BaseHttpService } from 'src/app/shared/base-http.service';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PredictedG4ApiService extends BaseHttpService {
  constructor(http: HttpClient) { super(http)}
    public pG4Records(e:string, species:string,sortcol:string,sortOrder:string, pageIndex = 0, pageSize = 10): Observable<any> {
    return this.getData('predicted', {
      query: e,
      species:species.replace(" ","_"),
      sortcol: sortcol,
      sort: sortOrder,
      page: pageIndex.toString(),
      size: pageSize.toString(),
    });
  }
  public downloadpG4Records(e:string, species:string): Observable<any> {
    return this.getData('predicted/download', {
      query: e,
      species:species
    });
  }

}
