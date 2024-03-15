import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ToastrService } from 'ngx-toastr';
import { UserService } from '../user.service';

@Component({
  selector: 'app-exam-question',
  templateUrl: './exam-question.component.html',
  styleUrls: ['./exam-question.component.css']
})
export class ExamQuestionComponent {
  questionCount: number = 10;
  questionOptions: number[] = [];
  questions: any[] = [];
  userData: any;
exam_data: any;
  exam_create_id: any;
  exam_actions: any;
 

  constructor(private http: HttpClient, 
              private toastr: ToastrService, 
              private userService: UserService) {}

  ngOnInit() {
    this.exam_data = this.userService.getExamData();
    this.exam_create_id = this.exam_data["exam_create_id"];
    this.userData = this.userService.getUserData();
    this.exam_actions = this.exam_data["actions"];
    if (this.exam_actions == 'edit')
    {
      this.retrieveExamQuestion();
    }
    this.updateQuestions(); // Initialize with at least one question
}

  updateQuestions() {
    const minQuestions = 10;
    const maxQuestions = 100;
    this.questionOptions = Array.from({ length: maxQuestions - minQuestions + 1 }, (_, i) => minQuestions + i);
    
    // Update questions based on the selected count
    const selectedCount = +this.questionCount;
    if (this.exam_actions == "create"){
      this.questions = Array.from({ length: selectedCount }, (_, i) => {
          return {
            description: '',
            options: [{ text: 'Option A' }, { text: 'Option B' }, { text: 'Option C' }, { text: 'Option D' }],
            correctAnswerIndex: null // Initially set to null
          };
        });
    }
  }

  removeOption(questionIndex: number, optionIndex: number) {
    const question = this.questions[questionIndex];
    if (optionIndex >= 0 && optionIndex < question.options.length) {
      question.options.splice(optionIndex, 1);
    }
  }

  getOptionLetter(index: number): string {
    return String.fromCharCode(65 + index);
  }

  submitForm() {
    console.log(this.questions)
    const formData = {
      "username": this.userData.username,
      "role": this.userData.role,
      "exam_create_id": this.exam_create_id,
      "questions": this.questions.map(question => {
        return {
          description: question.description,
          options: question.options.map((option: any) => option.text),
          correctAnswer: this.getOptionLetter(question.correctAnswerIndex)
        };
      })
    };
    
    this.http.post('http://127.0.0.1:8000/exam-question/', formData).subscribe((response: any) => {
      try {
        if (response.message === 'success') {
          this.toastr.success('Successfully Added', "Question Adding", {
            positionClass: 'toast-top-center',
          });
        } else {
          this.toastr.error(response.data, 'Adding Failed', {
            positionClass: 'toast-top-center',
          });
        }
      } catch (error) {
        this.toastr.error('Adding Failed', 'Try Again',{
          positionClass: 'toast-top-center',
        });
      }
    });
  }
  retrieveExamQuestion() {

    const formData = {
      "username": this.userData.username,
      "role": this.userData.role,
      "exam_create_id": this.exam_create_id
    };
    
    this.http.post('http://127.0.0.1:8000/exam-fetch/', formData).subscribe((response: any) => {
      try {
        if (response.message === 'success') {
          this.questionCount = response.data.no_of_questions
          this.questions = response.data.questions
        } else {
          this.toastr.error(response.data, 'Fetching Failed', {
            positionClass: 'toast-top-center',
          });
        }
      } catch (error) {
        this.toastr.error('Fetching Failed', 'Try Again',{
          positionClass: 'toast-top-center',
        });
      }
    });
  }
}
