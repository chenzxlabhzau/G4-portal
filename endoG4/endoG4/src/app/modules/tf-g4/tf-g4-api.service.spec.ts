import { TestBed } from '@angular/core/testing';

import { TfG4ApiService } from './tf-g4-api.service';

describe('TfG4ApiService', () => {
  let service: TfG4ApiService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(TfG4ApiService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
