import { ComponentFixture, TestBed } from '@angular/core/testing';

import { JobSeekerRegisterComponent } from './job-seeker-register.component';

describe('JobSeekerRegisterComponent', () => {
  let component: JobSeekerRegisterComponent;
  let fixture: ComponentFixture<JobSeekerRegisterComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [JobSeekerRegisterComponent]
    });
    fixture = TestBed.createComponent(JobSeekerRegisterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
