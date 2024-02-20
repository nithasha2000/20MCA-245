import { Component } from '@angular/core';

@Component({
  selector: 'app-exam-question',
  templateUrl: './exam-question.component.html',
  styleUrls: ['./exam-question.component.css']
})
export class ExamQuestionComponent {
  questionCount: number = 1;
  questionOptions: number[] = [];
  questions: any[] = [];

  ngOnInit() {
    this.updateQuestions(); // Initialize with at least one question
  }

  updateQuestions() {
    const minQuestions = 1;
    const maxQuestions = 100;
    this.questionOptions = Array.from({ length: maxQuestions - minQuestions + 1 }, (_, i) => minQuestions + i);
    
    // Update questions based on the selected count
    const selectedCount = +this.questionCount;
    this.questions = Array.from({ length: selectedCount }, (_, i) => {
      return {
        description: '',
        options: ['Option A', 'Option B', 'Option C', 'Option D']
      };
    });
  }

  removeOption(questionIndex: number, optionIndex: number) {
    const question = this.questions[questionIndex];
    if (optionIndex >= 0 && optionIndex < question.options.length) {
      question.options.splice(optionIndex, 1);
    }
  }
}
