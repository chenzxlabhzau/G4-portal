import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PredictedG4Component } from './predicted-g4.component';

describe('PredictedG4Component', () => {
  let component: PredictedG4Component;
  let fixture: ComponentFixture<PredictedG4Component>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PredictedG4Component ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PredictedG4Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
