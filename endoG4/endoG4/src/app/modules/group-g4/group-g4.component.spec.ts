import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GroupG4Component } from './group-g4.component';

describe('GroupG4Component', () => {
  let component: GroupG4Component;
  let fixture: ComponentFixture<GroupG4Component>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ GroupG4Component ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(GroupG4Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
