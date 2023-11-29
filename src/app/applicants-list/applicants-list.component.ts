import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { ToastrService } from 'ngx-toastr';
import { UserService } from '../user.service';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import * as pako from 'pako';

@Component({
  selector: 'app-applicants-list',
  templateUrl: './applicants-list.component.html',
  styleUrls: ['./applicants-list.component.css']
})
export class ApplicantsListComponent implements OnInit {
  userData: any;
  users: any[] = [];
  job_data: any;
  job_id!: string
  @Output() featureSelected = new EventEmitter<any>();

  constructor(
    private http: HttpClient,
    private toastr: ToastrService,
    private userService: UserService,
    private router: Router
  ) {
    this.job_data = this.userService.getJobPost();
    if (this.job_data && Object.keys(this.job_data).length !== 0) {
      this.job_id = this.job_data.job_post_id || '';
    }
  }

  isButtonDisabled(user: any): boolean {
    // Add logic based on user.status to determine if the button should be disabled
    return user.status === 'rejected';
  }

  getStatusText(user: any): string {
    // Add logic based on user.status to determine the text displayed on the button
    switch (user.status) {
      case 'applied':
        return 'Shortlist';
      case 'shortlisted':
        return 'Reject';
      case 'rejected':
        return 'Rejected';
      default:
        return 'Unknown Status';
    }
  }

  ngOnInit() {
    this.userData = this.userService.getUserData();

    if (this.userData) {
      const payload = {
        "username": this.userData.username,
        "role": this.userData.role,
        "job_post_id": this.job_id
      };

      this.http.post('http://127.0.0.1:8000/view-applicants/', payload).subscribe((response: any) => {
      try {
        if (response.message === 'success') {
          this.users = response.data
        } 
        else if(response.data === 'Your are not authorized to view this page'){
          this.router.navigate(['/dashboard']);
          window.location.reload();
        }
        else {
          this.toastr.error(response.data, 'Failed to fetch applicants', {
            positionClass: 'toast-top-center',
          });
        }
      } catch (error) {
        this.toastr.error('Failed to fetch applicants', 'Try Again',{
          positionClass: 'toast-top-center',
        });
      }
    });
    }
  }

  viewUser(user: any) {
    console.log(user)
  }

  downloadResume(user: any){
    this.userData = this.userService.getUserData();

    if (this.userData) {
      const payload = {
        "username": this.userData.username,
        "role": this.userData.role,
        "job_seeker_id": user.job_seeker_id
      };

        this.http.post('http://127.0.0.1:8000/download_applicant_resume/', payload, { responseType: 'arraybuffer' })
        .subscribe(
          (response: ArrayBuffer) => {
            try {
              const decompressedData = pako.inflate(new Uint8Array(response));
              // Create a Blob from the ArrayBuffer
              const blob = new Blob([decompressedData], { type: 'application/pdf' });

              // Create a download link and trigger the download
              const link = document.createElement('a');
              link.href = window.URL.createObjectURL(blob);
              link.download = 'resume.pdf'; // specify the filename
              document.body.appendChild(link);
              link.click();
              document.body.removeChild(link);
            } catch (error) {
              this.toastr.error('Failed to process the file', 'Try Again', {
                positionClass: 'toast-top-center',
              });
            }
          },
          (error) => {
            console.error(error);
            this.toastr.error('Failed to download resume', 'Try Again', {
              positionClass: 'toast-top-center',
            });
          }
        );
      }
  }
  shortlistCandidate(user: any){
    if (this.isButtonDisabled(user)) {
      // Button is disabled, do nothing
      return;
    }
    this.userData = this.userService.getUserData();

    if (this.userData) {
      const payload = {
        "username": this.userData.username,
        "role": this.userData.role,
        "job_seeker_id": user.user,
        "job_id": this.job_id
      };

      this.http.post('http://127.0.0.1:8000/shortlist-candidate/', payload).subscribe((response: any) => {
      try {
        if (response.message === 'success') {
          this.userService.setLastEmittedData("applicants-list");
          location.reload();
        } 
        else if(response.data === 'Your are not authorized to view this page'){
          this.router.navigate(['/dashboard']);
          window.location.reload();
        }
        else {
          this.toastr.error(response.data, 'Failed to shortlist applicant', {
            positionClass: 'toast-top-center',
          });
        }
      } catch (error) {
        this.toastr.error('Failed to shortlist applicant', 'Try Again',{
          positionClass: 'toast-top-center',
        });
      }
    });
  }
  }
}
