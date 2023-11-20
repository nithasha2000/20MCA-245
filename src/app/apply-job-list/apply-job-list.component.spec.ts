import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ApplyJobListComponent } from './apply-job-list.component';

describe('ApplyJobListComponent', () => {
  let component: ApplyJobListComponent;
  let fixture: ComponentFixture<ApplyJobListComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ApplyJobListComponent]
    });
    fixture = TestBed.createComponent(ApplyJobListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
