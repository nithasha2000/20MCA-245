import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ExamWidgetComponent } from './exam-widget.component';

describe('ExamWidgetComponent', () => {
  let component: ExamWidgetComponent;
  let fixture: ComponentFixture<ExamWidgetComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ExamWidgetComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ExamWidgetComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
