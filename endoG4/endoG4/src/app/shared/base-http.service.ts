import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { map, catchError } from 'rxjs/operators';

import { environment } from '../../environments/environment';

@Injectable()
export class BaseHttpService {
  constructor(private http: HttpClient) {}

  public getData(route: string, data?: any): Observable<any> {
    return this.http.get(this._generateRoute(route, environment.apiURL), this._generateOptions(data));
  }

  private _generateRoute(route: string, envURL: string): string {
    return `${envURL}/${route}`;
  }
  public downloadFile(filePath,filename="search_result.csv"){
    var link=document.createElement('a');
    link.href = filePath;
    link.download = filename
    link.click();
  }

  private _generateOptions(data?: any): any {
    return { params: data };
  }
}
