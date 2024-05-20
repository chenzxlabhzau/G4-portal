import { CollectionViewer, DataSource } from '@angular/cdk/collections';
import { Observable, BehaviorSubject, of } from 'rxjs';
import { catchError, tap, map, finalize } from 'rxjs/operators';
import { CellTypeService } from '../cell-type.service';
import {G4SampleRecord} from "src/app/shared/model/g4-sample";



export class G4TableDatasource implements DataSource<G4SampleRecord> {
  private G4RecordSubject = new BehaviorSubject<G4SampleRecord[]>([]);
  private loadingSubject = new BehaviorSubject<boolean>(false);
  public loading$ = this.loadingSubject.asObservable();
  public resultLength: number | undefined;

  constructor(private dataApiService: CellTypeService) {}
  loadG4SampleRecords(sample:string, query:string ,sortcol:string,sortOrder:string, pageIndex: number, pageSize: number) {
    this.loadingSubject.next(true);

    this.dataApiService
      .SampleRecords(sample, query,sortcol,sortOrder, pageIndex, pageSize)
      .pipe(
        tap((val) => {
          this.resultLength = val.count;
        }),
        map((res) => res.result),
        catchError(() => of([])),
        finalize(() => this.loadingSubject.next(false))
      )
      .subscribe((rnas) => this.G4RecordSubject.next(rnas));
  }


  connect(collectionViewer: CollectionViewer): Observable<G4SampleRecord[]> {
    return this.G4RecordSubject.asObservable();
  }

  disconnect(collectionViewer: CollectionViewer): void {
    this.G4RecordSubject.complete();
    this.loadingSubject.complete();
  }
}
