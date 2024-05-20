import { CollectionViewer, DataSource } from '@angular/cdk/collections';
import { Observable, BehaviorSubject, of } from 'rxjs';
import { catchError, tap, map, finalize } from 'rxjs/operators';
import { EpigeneticsService } from './epigenetics.service';
import { Samplerecord } from "src/app/shared/model/Sample-record";


export class SampleDataSource implements DataSource<Samplerecord> {
  private SampleRecordSubject = new BehaviorSubject<Samplerecord[]>([]);

  private loadingSubject = new BehaviorSubject<boolean>(false);

  public loading$ = this.loadingSubject.asObservable();
  public resultLength: number | undefined;

  constructor(private dataApiService: EpigeneticsService) {}

  loadSampleRecords(query: string, sortcol:string,sortOrder:string, pageIndex: number, pageSize: number) {
    this.loadingSubject.next(true);

    this.dataApiService
      .SampleRecords(query,sortcol,sortOrder, pageIndex, pageSize)
      .pipe(
        tap((val) => {
          this.resultLength = val.count;
        }),
        map((res) => res.result),
        catchError(() => of([])),
        finalize(() => this.loadingSubject.next(false))
      )
      .subscribe((rnas) => this.SampleRecordSubject.next(rnas));
  }

  connect(collectionViewer: CollectionViewer): Observable<Samplerecord[]> {
    return this.SampleRecordSubject.asObservable();
  }

  disconnect(collectionViewer: CollectionViewer): void {
    this.SampleRecordSubject.complete();
    this.loadingSubject.complete();
  }
}
