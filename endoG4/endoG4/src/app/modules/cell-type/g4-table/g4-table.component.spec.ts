import { ComponentFixture, TestBed } from '@angular/core/testing';

import { G4TableComponent } from './g4-table.component';

describe('G4TableComponent', () => {
  let component: G4TableComponent;
  let fixture: ComponentFixture<G4TableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ G4TableComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(G4TableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
