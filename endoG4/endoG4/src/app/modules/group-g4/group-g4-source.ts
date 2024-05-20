import { CollectionViewer, DataSource } from '@angular/cdk/collections';
import { Observable, BehaviorSubject, of } from 'rxjs';
import { catchError, tap, map, finalize } from 'rxjs/operators';
import { GroupG4ApiService } from './group-g4-api.service';
import {eG4record} from "src/app/shared/model/eg4-record";


export class eG4DataSource implements DataSource<eG4record> {
  private eG4RecordSubject = new BehaviorSubject<eG4record[]>([]);

  private loadingSubject = new BehaviorSubject<boolean>(false);

  public loading$ = this.loadingSubject.asObservable();
  public resultLength: number | undefined;

  constructor(private dataApiService: GroupG4ApiService) {}

  loadpG4Records(query: string, species:string, group:string, sortcol:string,sortOrder:string, pageIndex: number, pageSize: number) {
    this.loadingSubject.next(true);

    this.dataApiService
      .eG4Records(query,species,group,sortcol,sortOrder, pageIndex, pageSize)
      .pipe(
        tap((val) => {
          this.resultLength = val.count;
        }),
        map((res) => res.result),
        catchError(() => of([])),
        finalize(() => this.loadingSubject.next(false))
      )
      .subscribe((rnas) => this.eG4RecordSubject.next(rnas));
  }

  connect(collectionViewer: CollectionViewer): Observable<eG4record[]> {
    return this.eG4RecordSubject.asObservable();
  }

  disconnect(collectionViewer: CollectionViewer): void {
    this.eG4RecordSubject.complete();
    this.loadingSubject.complete();
  }
}
