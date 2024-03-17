import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { ToastrService } from 'ngx-toastr';
import { UserService } from '../user.service';

@Component({
  selector: 'app-exam-view',
  templateUrl: './exam-view.component.html',
  styleUrls: ['./exam-view.component.css']
})
export class ExamViewComponent {
  questions: any[] = [];
  exam_data: any;
  exam_name: any;
  exam_create_id: any;
  userData: any;
  exam_actions: any;
  questionCount: any;

  constructor(private http: HttpClient, 
    private toastr: ToastrService, 
    private userService: UserService) {}

    ngOnInit() {
      this.exam_data = this.userService.getExamData();
      this.exam_create_id = this.exam_data["exam_create_id"];
      this.userData = this.userService.getUserData();
      this.exam_actions = this.exam_data["actions"];
      if (this.exam_actions == 'view')
      {
        this.retrieveExamQuestion();
      }
  }

  getOptionLetter(index: number): string {
    // Assuming options are represented as an array of strings
    const letters = ['A', 'B', 'C', 'D']; // Add more letters if needed
    return letters[index] || ''; // Returns the corresponding letter or an empty string if index is out of bounds
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
            this.exam_name = response.data.exam_name
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

    cancel(){
      this.userService.setNavItemData("app-exam-table")
      this.userService.setLastEmittedData("app-exam-table");
      location.reload();
    }
}
