import { CollectionViewer, DataSource } from '@angular/cdk/collections';
import { Observable, BehaviorSubject, of } from 'rxjs';
import { catchError, tap, map, finalize } from 'rxjs/operators';
import { EpiApiService } from '../epi-api.service';
import {dhsRecord} from "src/app/shared/model/dhs-record";


export class dhsDataSource implements DataSource<dhsRecord> {
  private dhsRecordSubject = new BehaviorSubject<dhsRecord[]>([]);

  private loadingSubject = new BehaviorSubject<boolean>(false);

  public loading$ = this.loadingSubject.asObservable();
  public resultLength: number | undefined;

  constructor(private dataApiService: EpiApiService) {}

  loaddhsRecords(sample: string, query:string, sortcol:string,sortOrder:string, pageIndex: number, pageSize: number) {
    this.loadingSubject.next(true);

    this.dataApiService
      .dhsRecords(sample,query,sortcol,sortOrder, pageIndex, pageSize)
      .pipe(
        tap((val) => {
          this.resultLength = val.count;
        }),
        map((res) => res.result),
        catchError(() => of([])),
        finalize(() => this.loadingSubject.next(false))
      )
      .subscribe((rnas) => this.dhsRecordSubject.next(rnas));
  }

  connect(collectionViewer: CollectionViewer): Observable<dhsRecord[]> {
    return this.dhsRecordSubject.asObservable();
  }

  disconnect(collectionViewer: CollectionViewer): void {
    this.dhsRecordSubject.complete();
    this.loadingSubject.complete();
  }
}
