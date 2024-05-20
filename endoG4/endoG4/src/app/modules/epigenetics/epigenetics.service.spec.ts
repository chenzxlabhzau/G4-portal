import { TestBed } from '@angular/core/testing';

import { EpigeneticsService } from './epigenetics.service';

describe('EpigeneticsService', () => {
  let service: EpigeneticsService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(EpigeneticsService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
