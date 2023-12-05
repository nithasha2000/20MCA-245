import { Component } from '@angular/core';

@Component({
  selector: 'app-exam-question',
  templateUrl: './exam-question.component.html',
  styleUrls: ['./exam-question.component.css']
})
export class ExamQuestionComponent {
 selectedQuestionType: string = 'multipleChoice';
}
