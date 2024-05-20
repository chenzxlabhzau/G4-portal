import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DhsComponent } from './dhs.component';

describe('DhsComponent', () => {
  let component: DhsComponent;
  let fixture: ComponentFixture<DhsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DhsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DhsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
