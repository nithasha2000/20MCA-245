import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { UserService } from '../user.service';

@Component({
  selector: 'app-result',
  templateUrl: './result.component.html',
  styleUrls: ['./result.component.css']
})
export class ResultComponent implements OnInit {
  score: any;
  time: any;
  correct_answers: any;
  wrong_answers: any;
  unattended: any;
  userData: any;
  exams: any;

  constructor(
    private http: HttpClient,
    private router: Router, 
    private toastr: ToastrService, 
    private userService: UserService
  ) {}

  ngOnInit() {
    this.userData = this.userService.getUserData();
    this.exams= this.userService.getExamAttend();
    this.retrieveExamResult()
  }

  formatTime(totalSeconds: number): string {
    const hours = Math.floor(totalSeconds / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const seconds = totalSeconds % 60;

    // Ensure each part has two digits
    const formattedHours = ('0' + hours).slice(-2);
    const formattedMinutes = ('0' + minutes).slice(-2);
    const formattedSeconds = ('0' + seconds).slice(-2);

    return `${formattedHours}:${formattedMinutes}:${formattedSeconds}`;
}

  retrieveExamResult() {
    const formData = {
      "username": this.userData.username,
      "role": this.userData.role,
      "exam_create_id": this.exams.exam_create_id
    };
    
    this.http.post('http://127.0.0.1:8000/exam-result/', formData).subscribe((response: any) => {
      try {
        if (response.message === 'success') {
          this.score = response.data.score;
          this.time = this.formatTime(response.data.time_left);
          this.correct_answers = response.data.correct_answers;
          this.wrong_answers = response.data.wrong_answers;
          this.unattended = response.data.unattended;
          this.userService.removeExamAttend();
        }
        else {
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
  ok(){
    this.router.navigate(['/exam-widget']);
  }
}
