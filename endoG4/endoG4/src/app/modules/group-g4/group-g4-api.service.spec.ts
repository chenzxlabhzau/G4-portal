import { TestBed } from '@angular/core/testing';

import { GroupG4ApiService } from './group-g4-api.service';

describe('GroupG4ApiService', () => {
  let service: GroupG4ApiService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(GroupG4ApiService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
