import { Component } from '@angular/core';

@Component({
  selector: 'app-register-job-seeker',
  templateUrl: './register-job-seeker.component.html',
  styleUrls: ['./register-job-seeker.component.css']
})
export class RegisterJobSeekerComponent {
  fullName: string = '';
  email: string = '';
  password: string = '';
  education: string = '';
  workExperience: string = '';

  onFileSelected(event: any) {
    // Handle file selection (if needed)
  }

  onSubmit() {
    // Implement job seeker registration logic here
    console.log('Job Seeker Form submitted');
    console.log('Full Name:', this.fullName);
    console.log('Email:', this.email);
    console.log('Password:', this.password);
    console.log('Education Background:', this.education);
    console.log('Work Experience:', this.workExperience);
  }
}

