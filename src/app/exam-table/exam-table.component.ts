import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { ToastrService } from 'ngx-toastr';
import { UserService } from '../user.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-exam-table',
  templateUrl: './exam-table.component.html',
  styleUrls: ['./exam-table.component.css']
})

export class ExamTableComponent implements OnInit {
exams: any[] = [];
userData: any;
constructor(
    private http: HttpClient,
    private toastr: ToastrService,
    private userService: UserService,
    private router: Router,
  ) {}

ngOnInit() {
  this.userData = this.userService.getUserData();

    if (this.userData) {
      const payload = {
        "username": this.userData.username,
        "role": this.userData.role
      };
    
      this.http.post('http://127.0.0.1:8000/view-exam-list',payload).subscribe((response: any) => {
      try {
        if (response.message === 'success') {
          this.exams = response.data
        } 
        else if(response.data === 'Your are not authorized to view this page'){
          this.router.navigate(['/dashboard']);
          window.location.reload();
        }
        else {
          this.toastr.error(response.data, 'Failed to fetch view job list', {
            positionClass: 'toast-top-center',
          });
        }
      } catch (error) {
        this.toastr.error('Failed to fetch view job list', 'Try Again',{
          positionClass: 'toast-top-center',
        });
      }
    });
    }
}
 handleAdd() {
  this.router.navigate(['/exam-question']); // Navigate to the 'target' route
}

  }

