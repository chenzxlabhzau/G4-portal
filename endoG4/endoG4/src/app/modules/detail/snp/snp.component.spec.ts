import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SnpComponent } from './snp.component';

describe('SnpComponent', () => {
  let component: SnpComponent;
  let fixture: ComponentFixture<SnpComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SnpComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SnpComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
