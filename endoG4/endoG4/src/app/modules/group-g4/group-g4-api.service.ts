import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BaseHttpService } from 'src/app/shared/base-http.service';
import { Observable } from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class GroupG4ApiService extends BaseHttpService{
  constructor(http: HttpClient) { super(http)}
  public eG4Records(e:string,species:string, group:string,sortcol:string,sortOrder:string, pageIndex = 0, pageSize = 10): Observable<any> {
    return this.getData('group', {
      query: e,
      species:species,
      group:group,
      sortcol: sortcol,
      sort: sortOrder,
      page: pageIndex.toString(),
      size: pageSize.toString(),
    });
  }
  public downloadeG4Records(e:string, species:string, group:string): Observable<any> {
    return this.getData('group/download', {
      query: e,
      species:species,
      group:group
    });
  }
}
