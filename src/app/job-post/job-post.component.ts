import { HttpClient } from '@angular/common/http';
import { Component, EventEmitter, Output } from '@angular/core';
import { ToastrService } from 'ngx-toastr';
import { UserService } from '../user.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-job-post',
  templateUrl: './job-post.component.html',
  styleUrls: ['./job-post.component.css']
})
export class JobPostComponent {
  currentDate: string;
  job_title!: string;
  job_description!: string;
  experience!: string;
  location!: string;
  salary_range!: string;
  application_deadline!: string;
  userData!: any;
  job_data!: any;
  softSkills: any = {};

  @Output() featureSelected = new EventEmitter<any>();

  constructor(
    private http: HttpClient,
    private toastr: ToastrService,
    private userService: UserService,
    private router: Router
  ) {
    this.userData = this.userService.getUserData();
    this.job_data = this.userService.getJobPost();
    if (this.job_data && Object.keys(this.job_data).length !== 0) {

      // If job_data is present, fill the form fields
      this.job_title = this.job_data.job_title || '';
      this.job_description = this.job_data.job_description || '';
      this.experience = this.job_data.experience || '';
      this.location = this.job_data.location || '';
      this.softSkills = this.job_data.soft_skills || {};
      this.salary_range = this.job_data.salary_range || '';
      this.application_deadline = this.job_data.application_deadline || '';
    }
    const today = new Date();
    const dd = String(today.getDate()).padStart(2, '0');
    const mm = String(today.getMonth() + 1).padStart(2, '0'); 
    const yyyy = today.getFullYear();
    this.currentDate = yyyy + '-' + mm + '-' + dd;
  }

  job_post(){
    const formData = new FormData();
    // Add form data fields
    if (this.job_data && Object.keys(this.job_data).length !== 0){
      formData.append('type', 'edit');
      formData.append('job_post_id', this.job_data.job_post_id);
    }
    else{
      formData.append('type', 'create');
    }
    formData.append('user_data', JSON.stringify(this.userData));
    formData.append('job_title', this.job_title);
    formData.append('job_description', this.job_description);
    formData.append('experience', this.experience);
    formData.append('location', this.location);
    formData.append('soft_skills', JSON.stringify(this.softSkills));
    formData.append('salary_range', this.salary_range);
    formData.append('application_deadline', this.application_deadline);
    this.http.post('http://127.0.0.1:8000/job-post/', formData).subscribe((response: any) => {
      try {
        if (response.message === 'success') {
          if (this.job_data && Object.keys(this.job_data).length !== 0){
            this.toastr.success('Job Edited', 'Job Edited Successfully', {
              positionClass: 'toast-top-center',
            });
            this.userService.removeJobPost();
            this.featureSelected.emit("job-post-widget");
          }
          else{
            this.toastr.success('Job Posted', 'Job Posted Successfully', {
              positionClass: 'toast-top-center',
            });
            this.featureSelected.emit("job-post-widget");
          }
        } 
        else {
          if (Array.isArray(response.data)) {
            response.data.forEach((item: any) => {
              if (this.job_data && Object.keys(this.job_data).length !== 0){
                this.toastr.error(item, 'Job editing Failed', {
                  positionClass: 'toast-top-center',
                });
              }
              else{
                this.toastr.error(item, 'Job posting Failed', {
                  positionClass: 'toast-top-center',
                });
              }
            });
          } else {
            if (this.job_data && Object.keys(this.job_data).length !== 0){
              this.toastr.error(response.data, 'Job Editing Failed', {
                positionClass: 'toast-top-center',
              });
            }
            else{
              this.toastr.error(response.data, 'Job Posting Failed', {
                positionClass: 'toast-top-center',
              });
            }
          }
        }
      } catch (error) {
        if (this.job_data && Object.keys(this.job_data).length !== 0){
          this.toastr.error('Job Editing Failed', 'Try Again',{
            positionClass: 'toast-top-center',
          });
        }
        else{
          this.toastr.error('Job Posting Failed', 'Try Again',{
            positionClass: 'toast-top-center',
          });
        }
      }
    });
  }
}
