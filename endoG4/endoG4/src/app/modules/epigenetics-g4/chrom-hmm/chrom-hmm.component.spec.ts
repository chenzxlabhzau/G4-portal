import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ChromHMMComponent } from './chrom-hmm.component';

describe('ChromHMMComponent', () => {
  let component: ChromHMMComponent;
  let fixture: ComponentFixture<ChromHMMComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ChromHMMComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ChromHMMComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
