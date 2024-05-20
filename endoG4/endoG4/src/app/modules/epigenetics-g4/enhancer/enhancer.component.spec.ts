import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EnhancerComponent } from './enhancer.component';

describe('EnhancerComponent', () => {
  let component: EnhancerComponent;
  let fixture: ComponentFixture<EnhancerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ EnhancerComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(EnhancerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
