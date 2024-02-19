import { Component } from '@angular/core';

@Component({
  selector: 'app-exam-question',
  templateUrl: './exam-question.component.html',
  styleUrls: ['./exam-question.component.css']
})
export class ExamQuestionComponent {
  questionCount: number = 1;

  getQuestionArray(): number[] {
    return Array.from({ length: this.questionCount }, (_, i) => i + 1);
  }

  removeOption(questionIndex: number, option: string) {
    const optionIndex = option === 'C' ? 2 : 3; // Calculate the index of the option to remove
    const questionElement = document.getElementById(`question_${questionIndex}`);
    if (questionElement) {
      const optionElements = questionElement.getElementsByClassName('form-group');
      if (optionElements && optionElements.length > optionIndex) {
        questionElement.removeChild(optionElements[optionIndex]);
      }
    }
  }
}
