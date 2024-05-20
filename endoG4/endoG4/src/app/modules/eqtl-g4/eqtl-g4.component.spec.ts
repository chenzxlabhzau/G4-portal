import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EqtlG4Component } from './eqtl-g4.component';

describe('EqtlG4Component', () => {
  let component: EqtlG4Component;
  let fixture: ComponentFixture<EqtlG4Component>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ EqtlG4Component ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(EqtlG4Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
