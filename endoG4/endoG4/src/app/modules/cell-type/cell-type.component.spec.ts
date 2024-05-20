import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CellTypeComponent } from './cell-type.component';

describe('CellTypeComponent', () => {
  let component: CellTypeComponent;
  let fixture: ComponentFixture<CellTypeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CellTypeComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CellTypeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
