import { TestBed } from '@angular/core/testing';

import { EqtlService } from './eqtl.service';

describe('EqtlService', () => {
  let service: EqtlService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(EqtlService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
