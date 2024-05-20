import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EpigeneticsComponent } from './epigenetics.component';

describe('EpigeneticsComponent', () => {
  let component: EpigeneticsComponent;
  let fixture: ComponentFixture<EpigeneticsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ EpigeneticsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(EpigeneticsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
