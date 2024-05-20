import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BaseHttpService } from 'src/app/shared/base-http.service';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DetailApiService extends BaseHttpService{

  constructor(http: HttpClient) { super(http)}
   public findG4BasicInfo(s: string): Observable<any> {
    return this.getData('detail/basic/' + s);
  }
   public findG4TF(s: string): Observable<any> {
    return this.getData('detail/tf/' + s);
  }
   public findG4SNP(s: string, eqtlType: string): Observable<any> {
    return this.getData('detail/snp', {
      g_id:s,
      eqtlType:eqtlType
    });
  }
  public findG4HMM(s: string): Observable<any> {
    return this.getData('detail/hmm/' + s);
  }
  public findG4DHS(s: string): Observable<any> {
    return this.getData('detail/dhs/' + s);
  }
  public findG4ENC(s: string): Observable<any> {
    return this.getData('detail/enhancer/' + s);
  }
  public findEnrichment(s:string):Observable<any> {
    return this.getData('detail/enrichment/' + s);
  }
}
