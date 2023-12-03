import { Component } from '@angular/core';

@Component({
  selector: 'app-exam-form',
  templateUrl: './exam-form.component.html',
  styleUrls: ['./exam-form.component.css']
})
export class ExamFormComponent {
  examName: string = '';
  duration: string = '';
  negativeMarking: string = '';
  submitBeforeTimer: string = 'yes';
  displayCountdown: string = 'yes';
}
