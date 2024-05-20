import { TestBed } from '@angular/core/testing';

import { PredictedG4ApiService } from './predicted-g4-api.service';

describe('PredictedG4ApiService', () => {
  let service: PredictedG4ApiService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(PredictedG4ApiService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
