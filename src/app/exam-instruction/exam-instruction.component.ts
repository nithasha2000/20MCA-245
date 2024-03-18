import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { UserService } from '../user.service';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-exam-instruction',
  templateUrl: './exam-instruction.component.html',
  styleUrls: ['./exam-instruction.component.css']
})
export class ExamInstructionComponent {
  userData: any;
  exams: any;
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
      this.exams= this.userService.getExamAttend()
    }
  }
  agree(){
    const formData = {
      "username": this.userData.username,
      "role": this.userData.role,
      "exam_create_id": this.exams.exam_create_id
    };
    
    this.http.post('http://127.0.0.1:8000/check-exam/', formData).subscribe((response: any) => {
      try {
        if (response.message === 'success') {
          if (response.data == "attended"){
            this.toastr.warning("Exam Already Attended", 'Already Attended', {
              positionClass: 'toast-top-center',
            });
            return;
          }
          this.userService.setExamAttend({"exam_create_id": this.exams.exam_create_id,
            "exam_name": this.exams.exam_name,
              "numberOfQuestions": this.exams.numberOfQuestions,
              "maximumMarks": this.exams.maximumMarks,
              "duration": this.exams.duration,
              "agreement": "true"});
          this.router.navigate(['/exam'])
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
