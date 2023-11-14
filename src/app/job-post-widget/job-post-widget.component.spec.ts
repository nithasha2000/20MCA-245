import { ComponentFixture, TestBed } from '@angular/core/testing';

import { JobPostWidgetComponent } from './job-post-widget.component';

describe('JobPostWidgetComponent', () => {
  let component: JobPostWidgetComponent;
  let fixture: ComponentFixture<JobPostWidgetComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [JobPostWidgetComponent]
    });
    fixture = TestBed.createComponent(JobPostWidgetComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
