import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CompanyMaincontentComponent } from './company-maincontent.component';

describe('CompanyMaincontentComponent', () => {
  let component: CompanyMaincontentComponent;
  let fixture: ComponentFixture<CompanyMaincontentComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [CompanyMaincontentComponent]
    });
    fixture = TestBed.createComponent(CompanyMaincontentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
