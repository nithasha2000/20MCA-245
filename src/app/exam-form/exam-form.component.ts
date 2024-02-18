import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ToastrService } from 'ngx-toastr';
import { UserService } from '../user.service';
import { Router } from '@angular/router';
import { CookieService } from 'ngx-cookie-service';

@Component({
  selector: 'app-exam-form',
  templateUrl: './exam-form.component.html',
  styleUrls: ['./exam-form.component.css']
})
export class ExamFormComponent {
  examName: string = '';
  durationType: string = '';
  hourDuration: string = '';
  minuteDuration: string = '';
  customMinuteDuration: number = 0;
  negativeMarking: string = '';
  
  constructor(private http: HttpClient, 
              private toastr: ToastrService, 
              private router: Router, 
              private userService: UserService,
              private cookieService: CookieService) {
  }

  durationTypeChanged() {
    if (this.durationType === 'Hours') {
      this.minuteDuration = ''; // Clear minute duration if it was previously selected
      this.customMinuteDuration = 0; // Reset custom minute duration
    } else if (this.durationType === 'Minutes') {
      this.hourDuration = ''; // Clear hour duration if it was previously selected
    }
  }

  isFormValid(): boolean {
    // Implement form validation logic if needed
    return true;
  }

  submitForm() {
    // Extract percentage from negative marking option
    let percentage: number;
    switch (this.negativeMarking) {
      case '25% of that question':
        percentage = 25;
        break;
      case '50% of that question':
        percentage = 50;
        break;
      case '75% of that question':
        percentage = 75;
        break;
      case '100% of that question':
        percentage = 100;
        break;
      default:
        percentage = 0;
    }

    let durationInMinutes: number;
    if (this.durationType === 'Hours') {
      durationInMinutes = parseInt(this.hourDuration) * 60;
    } else {
      durationInMinutes = parseInt(this.minuteDuration);
    }

    const formData = {
      name: this.examName,
      duration_hours: this.durationType === 'Hours' ? parseInt(this.hourDuration) : null,
      duration_minutes: this.durationType === 'Minutes' ? parseInt(this.minuteDuration) : null,
      negative_marking_percentage: percentage, // Use extracted percentage
    };
   console.log(formData);
    this.http.post('http://127.0.0.1:8000/exam-form/', formData).subscribe((response: any) => {
      try {
        if (response.message === 'success') {
          this.toastr.success('Successfully Added', "Email Verification", {
            positionClass: 'toast-top-center',
          });
        } else {
          this.toastr.error(response.data, 'Adding Failed', {
            positionClass: 'toast-top-center',
          });
        }
      } catch (error) {
        this.toastr.error('Adding Failed', 'Try Again',{
          positionClass: 'toast-top-center',
        });
      }
    });
  }
}
