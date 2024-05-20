import { TestBed } from '@angular/core/testing';

import { CellTypeService } from './cell-type.service';

describe('CellTypeService', () => {
  let service: CellTypeService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(CellTypeService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
