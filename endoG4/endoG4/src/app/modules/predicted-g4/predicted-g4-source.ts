import { CollectionViewer, DataSource } from '@angular/cdk/collections';
import { Observable, BehaviorSubject, of } from 'rxjs';
import { catchError, tap, map, finalize } from 'rxjs/operators';
import { PredictedG4ApiService } from './predicted-g4-api.service';
import {pG4record} from "src/app/shared/model/pg4-record";


export class pG4DataSource implements DataSource<pG4record> {
  private pG4RecordSubject = new BehaviorSubject<pG4record[]>([]);

  private loadingSubject = new BehaviorSubject<boolean>(false);

  public loading$ = this.loadingSubject.asObservable();
  public resultLength: number | undefined;

  constructor(private dataApiService: PredictedG4ApiService) {}

  loadpG4Records(query: string, species:string,sortcol:string,sortOrder:string, pageIndex: number, pageSize: number) {
    this.loadingSubject.next(true);

    this.dataApiService
      .pG4Records(query,species,sortcol,sortOrder, pageIndex, pageSize)
      .pipe(
        tap((val) => {
          this.resultLength = val.count;
        }),
        map((res) => res.result),
        catchError(() => of([])),
        finalize(() => this.loadingSubject.next(false))
      )
      .subscribe((rnas) => this.pG4RecordSubject.next(rnas));
  }

  connect(collectionViewer: CollectionViewer): Observable<pG4record[]> {
    return this.pG4RecordSubject.asObservable();
  }

  disconnect(collectionViewer: CollectionViewer): void {
    this.pG4RecordSubject.complete();
    this.loadingSubject.complete();
  }
}
