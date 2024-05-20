import { CollectionViewer, DataSource } from '@angular/cdk/collections';
import { Observable, BehaviorSubject, of } from 'rxjs';
import { catchError, tap, map, finalize } from 'rxjs/operators';
import { EpiApiService } from '../epi-api.service';
import {chromhmmRecord} from "src/app/shared/model/chromhmm-record";


export class chromhmmDataSource implements DataSource<chromhmmRecord> {
  private chromhmmRecordSubject = new BehaviorSubject<chromhmmRecord[]>([]);

  private loadingSubject = new BehaviorSubject<boolean>(false);

  public loading$ = this.loadingSubject.asObservable();
  public resultLength: number | undefined;

  constructor(private dataApiService: EpiApiService) {}

  loadchromhmmRecords(sample: string, query:string, sortcol:string,sortOrder:string, pageIndex: number, pageSize: number) {
    this.loadingSubject.next(true);

    this.dataApiService
      .chromRecords(sample,query,sortcol,sortOrder, pageIndex, pageSize)
      .pipe(
        tap((val) => {
          this.resultLength = val.count;
        }),
        map((res) => res.result),
        catchError(() => of([])),
        finalize(() => this.loadingSubject.next(false))
      )
      .subscribe((rnas) => this.chromhmmRecordSubject.next(rnas));
  }

  connect(collectionViewer: CollectionViewer): Observable<chromhmmRecord[]> {
    return this.chromhmmRecordSubject.asObservable();
  }

  disconnect(collectionViewer: CollectionViewer): void {
    this.chromhmmRecordSubject.complete();
    this.loadingSubject.complete();
  }
}
