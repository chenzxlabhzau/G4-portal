import { TestBed } from '@angular/core/testing';

import { EpiApiService } from './epi-api.service';

describe('EpiApiService', () => {
  let service: EpiApiService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(EpiApiService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
