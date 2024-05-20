import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EqtlTableComponent } from './eqtl-table.component';

describe('EqtlTableComponent', () => {
  let component: EqtlTableComponent;
  let fixture: ComponentFixture<EqtlTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ EqtlTableComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(EqtlTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
