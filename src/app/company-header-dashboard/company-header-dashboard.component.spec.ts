import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CompanyHeaderDashboardComponent } from './company-header-dashboard.component';

describe('CompanyHeaderDashboardComponent', () => {
  let component: CompanyHeaderDashboardComponent;
  let fixture: ComponentFixture<CompanyHeaderDashboardComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [CompanyHeaderDashboardComponent]
    });
    fixture = TestBed.createComponent(CompanyHeaderDashboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
