import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ToastrService } from 'ngx-toastr';
import { FormControl, Validators } from '@angular/forms';

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
  marksEach = new FormControl('', [Validators.required, Validators.min(1)]);
  /*examNameControl = new FormControl('', [
    Validators.required,
    Validators.pattern('[a-zA-Z ]*')
  ]);*/


  constructor(private http: HttpClient, 
              private toastr: ToastrService) {
  }

  isFormValid(): boolean {
    return true;
  }

  submitForm() {
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
    } else{
      durationInMinutes = parseInt(this.minuteDuration);
    }
    const formData = {
      name: this.examName,
      duration_minutes: durationInMinutes,
      negative_marking_percentage: percentage, 
      marksEach: this.marksEach.value
    };
  
    this.http.post('http://127.0.0.1:8000/exam-form/', formData).subscribe((response: any) => {
      try {
        if (response.message === 'success') {
          this.toastr.success('Successfully Added', "Exam Details", {
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
