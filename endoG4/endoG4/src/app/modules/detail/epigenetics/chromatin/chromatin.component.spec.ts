import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ChromatinComponent } from './chromatin.component';

describe('ChromatinComponent', () => {
  let component: ChromatinComponent;
  let fixture: ComponentFixture<ChromatinComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ChromatinComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ChromatinComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
