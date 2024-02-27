import { HttpClient } from '@angular/common/http';
import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { ToastrService } from 'ngx-toastr';
import { UserService } from '../user.service';
import { Router } from '@angular/router';
import { ReloadService } from '../reload.service';

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
    private reloadService: ReloadService
  ) {}

ngOnInit() {
  this.userData = this.userService.getUserData();
    if (this.userData) {
      const payload = {
        "username": this.userData.username,
        "role": this.userData.role
      };
    
      this.http.post('http://127.0.0.1:8000/view-exam-list/',payload).subscribe((response: any) => {
      try {
        if (response.message === 'success') {
          this.exams = response.data
        } 
        else if(response.data === 'Your are not authorized to view this page'){
          this.router.navigate(['/dashboard']);
          window.location.reload();
        }
        else {
          this.toastr.error(response.data, 'Failed to fetch view exam details', {
            positionClass: 'toast-top-center',
          });
        }
      } catch (error) {
        this.toastr.error('Failed to fetch view exam details', 'Try Again',{
          positionClass: 'toast-top-center',
        });
      }
    });
    }
    else{
      this.toastr.error("Please login", 'Authentication Failed', {
            positionClass: 'toast-top-center',
      });
      this.router.navigate(['/login']);
    }
}
 @Output() featureSelected = new EventEmitter<String>();
  onSelect(feature: string){
    this.reloadService.triggerReload();
    this.featureSelected.emit(feature);
  }

  }

