import { CollectionViewer, DataSource } from '@angular/cdk/collections';
import { Observable, BehaviorSubject, of } from 'rxjs';
import { catchError, tap, map, finalize } from 'rxjs/operators';
import { TfG4ApiService } from './tf-g4-api.service';
import {pG4record} from "src/app/shared/model/pg4-record";


export class TFDataSource implements DataSource<pG4record> {
  private TFRecordSubject = new BehaviorSubject<pG4record[]>([]);

  private loadingSubject = new BehaviorSubject<boolean>(false);

  public loading$ = this.loadingSubject.asObservable();
  public resultLength: number | undefined;

  constructor(private dataApiService: TfG4ApiService) {}

  loadTFRecords(query: string,sortcol:string,sortOrder:string, pageIndex: number, pageSize: number) {
    this.loadingSubject.next(true);

    this.dataApiService
      .TFRecords(query,sortcol,sortOrder, pageIndex, pageSize)
      .pipe(
        tap((val) => {
          this.resultLength = val.count;
        }),
        map((res) => res.result),
        catchError(() => of([])),
        finalize(() => this.loadingSubject.next(false))
      )
      .subscribe((rnas) => this.TFRecordSubject.next(rnas));
  }

  connect(collectionViewer: CollectionViewer): Observable<pG4record[]> {
    return this.TFRecordSubject.asObservable();
  }

  disconnect(collectionViewer: CollectionViewer): void {
    this.TFRecordSubject.complete();
    this.loadingSubject.complete();
  }
}
