import { TestBed } from '@angular/core/testing';

import { DetailApiService } from './detail-api.service';

describe('DetailApiService', () => {
  let service: DetailApiService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(DetailApiService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
