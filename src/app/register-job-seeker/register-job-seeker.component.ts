import { Component } from '@angular/core';

@Component({
  selector: 'app-register-job-seeker',
  templateUrl: './register-job-seeker.component.html',
  styleUrls: ['./register-job-seeker.component.css']
})
export class RegisterJobSeekerComponent {
  // Define properties for form fields
  firstName!: string;
  lastName!: string;
  dob!: Date;
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
  experienceType!: string;
  jobTitle!: string;
  companyName!: string;
  startDate!: Date;
  endDate!: Date;
  

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
    // Handle form submission, e.g., send data to the server
    // You can access all the form fields' values from this component
    console.log('Form submitted', this);
  }
}
