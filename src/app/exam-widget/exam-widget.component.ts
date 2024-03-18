import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { UserService } from '../user.service';

@Component({
  selector: 'app-exam-widget',
  templateUrl: './exam-widget.component.html',
  styleUrls: ['./exam-widget.component.css']
})
export class ExamWidgetComponent implements OnInit{
  userData: any;
  exams: any = [];
  constructor(
    private http: HttpClient,
    private router: Router, 
    private toastr: ToastrService, 
    private userService: UserService){}

  ngOnInit() {
    this.userData = this.userService.getUserData();
    if(!this.userData){
      this.toastr.warning("Please login before continuing", 'Login Required', {
        positionClass: 'toast-top-center',
      });
      this.userService.setExamClick();
      this.router.navigate(['/login'])
    }
    else{
      this.retrieveExams()
    }
  }

  navigateToExam(exam:any){
    this.userService.setExamAttend({
      "exam_create_id": exam.exam_create_id, 
      "exam_name": exam.title,
      "numberOfQuestions": exam.numberOfQuestions,
      "maximumMarks": exam.maximumMarks,
      "duration": exam.duration,
      "agreement": "false"});
    this.router.navigate(['/exam-instruction'])
  }

  retrieveExams() {

    const formData = {
      "username": this.userData.username,
      "role": this.userData.role
    };
    
    this.http.post('http://127.0.0.1:8000/exams/', formData).subscribe((response: any) => {
      try {
        if (response.message === 'success') {
          this.exams = response.data
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
