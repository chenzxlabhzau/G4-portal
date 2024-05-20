import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TfG4Component } from './tf-g4.component';

describe('TfG4Component', () => {
  let component: TfG4Component;
  let fixture: ComponentFixture<TfG4Component>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TfG4Component ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(TfG4Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
