import { CollectionViewer, DataSource } from '@angular/cdk/collections';
import { Observable, BehaviorSubject, of } from 'rxjs';
import { catchError, tap, map, finalize } from 'rxjs/operators';
import { EqtlService } from './eqtl.service';
import { EqtlRecord } from "../../../shared/model/eqtl-record";


export class eqtlDataSource implements DataSource<EqtlRecord> {
  private eqtlRecordSubject = new BehaviorSubject<EqtlRecord[]>([]);

  private loadingSubject = new BehaviorSubject<boolean>(false);

  public loading$ = this.loadingSubject.asObservable();
  public resultLength: number | undefined;

  constructor(private dataApiService: EqtlService) {}

  loadeqtlRecords(query: string, eqtlType:string,sortcol:string,sortOrder:string, pageIndex: number, pageSize: number) {
    this.loadingSubject.next(true);

    this.dataApiService
      .eqtlRecords(query,eqtlType,sortcol,sortOrder, pageIndex, pageSize)
      .pipe(
        tap((val) => {
          this.resultLength = val.count;
        }),
        map((res) => res.result),
        catchError(() => of([])),
        finalize(() => this.loadingSubject.next(false))
      )
      .subscribe((rnas) => this.eqtlRecordSubject.next(rnas));
  }

  connect(collectionViewer: CollectionViewer): Observable<EqtlRecord[]> {
    return this.eqtlRecordSubject.asObservable();
  }

  disconnect(collectionViewer: CollectionViewer): void {
    this.eqtlRecordSubject.complete();
    this.loadingSubject.complete();
  }
}
