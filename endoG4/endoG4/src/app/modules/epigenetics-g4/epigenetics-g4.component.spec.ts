import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EpigeneticsG4Component } from './epigenetics-g4.component';

describe('EpigeneticsG4Component', () => {
  let component: EpigeneticsG4Component;
  let fixture: ComponentFixture<EpigeneticsG4Component>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ EpigeneticsG4Component ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(EpigeneticsG4Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
