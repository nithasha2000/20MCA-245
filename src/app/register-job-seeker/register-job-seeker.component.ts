import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { FormBuilder, FormControl, FormGroup, FormsModule, Validators } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';
import { EncDecService } from '../encdec.service';

@Component({
  selector: 'app-register-job-seeker',
  templateUrl: './register-job-seeker.component.html',
  styleUrls: ['./register-job-seeker.component.css']
})
export class RegisterJobSeekerComponent {

  constructor(private http:HttpClient, private fb: FormBuilder, private toastr: ToastrService, private router: Router, private EncrDecr: EncDecService,)
  {

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
  jobTitle!: string;
  companyName!: string;
  startDate!: string; 
  endDate!: string;
  jobPassword!: string;
  confirm_jobPassword!: string;
  experienceType!: string;

  passwordValidator() {
    return (control: any) => {
      const value = control.value;
      const hasUppercase = /[A-Z]/.test(value);
      const hasLowercase = /[a-z]/.test(value);
      const hasDigit = /\d/.test(value);
      const hasSpecialChar = /[!@#$%^&*()_+{}\[\]:;<>,.?~\\/-]/.test(value);

      const isValid = hasUppercase && hasLowercase && hasDigit && hasSpecialChar;

      return isValid ? null : { invalidPassword: true };
    };
  }

  firstNameControl = new FormControl('', [
    Validators.required,
    Validators.pattern('[a-zA-Z ]*')
  ]);

  lastNameControl = new FormControl('', [
    Validators.required,
    Validators.pattern('[a-zA-Z ]*')
  ]);

  dobControl = new FormControl('', [
    Validators.required,
    Validators.pattern('[a-zA-Z]*')
  ]);

  phoneControl = new FormControl('', [
    Validators.required,
    Validators.pattern(/^\d{10}$/) // Adjust the pattern based on your requirements
  ]);
  emailControl = new FormControl('', [
    Validators.required,
    Validators.email
  ]);

  streetAddressLine1Control = new FormControl('', [
    Validators.required
  ]);

  cityControl = new FormControl('', [
    Validators.required
  ]);

  stateControl = new FormControl('', [
    Validators.required
  ]);

  highestQualificationControl = new FormControl('', [
    Validators.required
  ]);

  institutionControl = new FormControl('', [
    Validators.required
  ]);

  cgpaControl = new FormControl('', [
    Validators.required
  ]);

  experienceTypeControl = new FormControl('', [
    Validators.required
  ]);

  jobPasswordControl = new FormControl('', [
    Validators.required,
    this.passwordValidator(),
  ]);
  
  onFileSelected(event: any) {
    this.resume = event.target.files[0];
  }

  // Define a property to keep track of the current form page
  page: number = 1;

  // Define methods to navigate between form pages
  nextPage() {
    if (this.page === 1) {
      if (!this.firstName || !this.lastName || !this.dob || !this.gender) {
        this.toastr.error('Please fill in all required fields before proceeding to the next page.', 'Registration Failed', {
          positionClass: 'toast-top-center',
        });
        return;
      }
    } else if (this.page === 2) {
      if (!this.phone || !this.email || !this.streetAddressLine1 || !this.city || !this.state) {
        this.toastr.error('Please fill in all required fields before proceeding to the next page.', 'Registration Failed', {
          positionClass: 'toast-top-center',
        });
        return;
      }
    } else if (this.page === 3) {
      if (!this.highestQualification || !this.institution || !this.cgpa) {
        this.toastr.error('Please fill in all required fields before proceeding to the next page.', 'Registration Failed', {
          positionClass: 'toast-top-center',
        });
        return;
      }
    } else if (this.page === 4) {
      if (!this.resume || !this.experienceType) {
        this.toastr.error('Please fill in all required fields before proceeding to the next page.', 'Registration Failed', {
          positionClass: 'toast-top-center',
        });
        return;
      }
    }
  
    this.page++;
  }

  previousPage() {
    this.page--;
  }

  onSubmit() {

    if (!this.jobPassword || !this.confirm_jobPassword) {
      this.toastr.error('Please fill in all required fields before submitting the form.', 'Registration Failed', {
        positionClass: 'toast-top-center',
      });
      return;
    }
    if (this.jobPassword !== this.confirm_jobPassword) {
      this.toastr.error('Passwords do not match', 'Validation Error', {
        positionClass: 'toast-top-center',
      });
      return;
    }
    var token = '123456$#@$^@1ERF'
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
    formData.append('jobPassword', this.EncrDecr.set(token, this.jobPassword));
    formData.append('confirm_jobPassword', this.EncrDecr.set(token, this.confirm_jobPassword));
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
