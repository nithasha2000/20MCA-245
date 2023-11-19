import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { FormsModule } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-register-job-seeker',
  templateUrl: './register-job-seeker.component.html',
  styleUrls: ['./register-job-seeker.component.css']
})
export class RegisterJobSeekerComponent {

  constructor(private http:HttpClient, private toastr: ToastrService, private router: Router)
  {
    obj:String;
  }
  // Define properties for form fields
  firstName!: string;
  lastName!: string;
  dob!: string;
  gender!: string;
  phone!: string;
  email!: string;
  streetAddressLine1!: string;
  streetAddressLine2!: string;
  city!: string;
  state!: string;
  highestQualification!: string;
  institution!: string;
  cgpa!: number;
  resume: File | null = null;
  experienceType!: string;
  jobTitle!: string;
  companyName!: string;
  startDate!: string; 
  endDate!: string;
  jobPassword!: string;
  confirm_jobPassword!: string;
  
  onFileSelected(event: any) {
    this.resume = event.target.files[0];
  }

  // Define a property to keep track of the current form page
  page: number = 1;

  // Define methods to navigate between form pages
  nextPage() {
    this.page++;
  }

  previousPage() {
    this.page--;
  }

  onSubmit() {
    const formData = new FormData();
    // Add form data fields
    formData.append('type', 'job_seeker_reg');
    formData.append('firstName', this.firstName);
    formData.append('lastName', this.lastName);
    formData.append('dob', this.dob);
    formData.append('gender', this.gender);
    formData.append('phone', this.phone);
    formData.append('email', this.email);
    formData.append('streetAddressLine1', this.streetAddressLine1);
    formData.append('streetAddressLine2', this.streetAddressLine2);
    formData.append('city', this.city);
    formData.append('state', this.state);
    formData.append('highestQualification', this.highestQualification);
    formData.append('institution', this.institution);
    formData.append('cgpa', this.cgpa.toString());
    formData.append('experienceType', this.experienceType);
    formData.append('jobTitle', this.jobTitle);
    formData.append('companyName', this.companyName);
    formData.append('startDate', this.startDate);
    formData.append('endDate', this.endDate);
    formData.append('jobPassword', this.jobPassword);
    formData.append('confirm_jobPassword', this.confirm_jobPassword);
    if (this.resume) {
      formData.append('resume', this.resume, this.resume.name);
    }

    this.http.post('http://127.0.0.1:8000/register/', formData).subscribe((response: any) => {
      try {
        if (response.message === 'success') {
          this.toastr.success('Account Registered', 'Registration Successful', {
            positionClass: 'toast-top-center',
          });
          this.router.navigate(['/login']);
        } else {
          if (Array.isArray(response.data)) {
            response.data.forEach((item: any) => {
              this.toastr.error(item, 'Registration Failed', {
                positionClass: 'toast-top-center',
              });
            });
          } else {
            this.toastr.error(response.data, 'Registration Failed', {
              positionClass: 'toast-top-center',
            });
          }
        }
      } catch (error) {
        this.toastr.error('Registration Failed', 'Try Again',{
          positionClass: 'toast-top-center',
        });
      }
    });
  }
}
