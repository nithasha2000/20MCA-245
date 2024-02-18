import { Component } from '@angular/core';

@Component({
  selector: 'app-exam-question',
  templateUrl: './exam-question.component.html',
  styleUrls: ['./exam-question.component.css']
})
export class ExamQuestionComponent {
  rowCount: number = 1;
  numbers: number[] = Array.from({length: 10}, (_, i) => i + 1);
  options: string[] = [];

  addRows() {
    for (let i = 0; i < this.rowCount; i++) {
      this.options.push('New Option');
    }
  }

  removeOption(index: number) {
    this.options.splice(index, 1);
  }
}
