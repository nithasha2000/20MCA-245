import { Component } from '@angular/core';


@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent{
currentSection = 1; 
  formData = {
    companyName: '',
    companyType: '',
    address: '',
    phone: '',
    email: '',
    profile: '',
    website: '',
    licenseNo: '',
    businessLicense: '',
    companyUsername: '',
    companyPassword: ''
  };

    nextSection() {
    if (this.currentSection < 6) {
      this.currentSection++;
    }
  }

  prevSection() {
    if (this.currentSection > 1) {
      this.currentSection--;
    }
  }

  onSubmit() {
    // Handle form submission here
    console.log('Form submitted:', this.formData);
  }

}

   

