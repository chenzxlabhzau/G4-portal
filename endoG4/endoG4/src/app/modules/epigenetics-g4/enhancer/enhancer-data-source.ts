import { CollectionViewer, DataSource } from '@angular/cdk/collections';
import { Observable, BehaviorSubject, of } from 'rxjs';
import { catchError, tap, map, finalize } from 'rxjs/operators';
import { EpiApiService } from '../epi-api.service';
import {enhancerRecord} from "src/app/shared/model/enhancer-record";


export class enhancerDataSource implements DataSource<enhancerRecord> {
  private enhancerRecordSubject = new BehaviorSubject<enhancerRecord[]>([]);

  private loadingSubject = new BehaviorSubject<boolean>(false);

  public loading$ = this.loadingSubject.asObservable();
  public resultLength: number | undefined;

  constructor(private dataApiService: EpiApiService) {}

  loadenhancerRecords(sample: string, query:string, sortcol:string,sortOrder:string, pageIndex: number, pageSize: number) {
    this.loadingSubject.next(true);

    this.dataApiService
      .enhancerRecords(sample,query,sortcol,sortOrder, pageIndex, pageSize)
      .pipe(
        tap((val) => {
          this.resultLength = val.count;
        }),
        map((res) => res.result),
        catchError(() => of([])),
        finalize(() => this.loadingSubject.next(false))
      )
      .subscribe((rnas) => this.enhancerRecordSubject.next(rnas));
  }

  connect(collectionViewer: CollectionViewer): Observable<enhancerRecord[]> {
    return this.enhancerRecordSubject.asObservable();
  }

  disconnect(collectionViewer: CollectionViewer): void {
    this.enhancerRecordSubject.complete();
    this.loadingSubject.complete();
  }
}
