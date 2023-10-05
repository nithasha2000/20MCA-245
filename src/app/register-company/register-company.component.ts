import { Component } from '@angular/core';

@Component({
  selector: 'app-register-company',
  templateUrl: './register-company.component.html',
  styleUrls: ['./register-company.component.css']
})
export class RegisterCompanyComponent {
companyName: string = '';
  companyType: string = '';
  address: string = '';
  phone: string = '';
  email: string = '';
  profile: string = '';
  website: string = '';
  licenseNo: string = '';
  businessLicense: string = '';
  companyUsername: string = '';
  companyPassword: string = '';

  onSubmit() {
    // Implement company registration logic here
    console.log('Company Form submitted');
    console.log('Company Name:', this.companyName);
    console.log('Company Type:', this.companyType);
    console.log('Address:', this.address);
    console.log('Phone Number:', this.phone);
    console.log('Email:', this.email);
    console.log('Company Profile:', this.profile);
    console.log('Company Website:', this.website);
    console.log('License Number:', this.licenseNo);
    console.log('Business License:', this.businessLicense);
    console.log('Username:', this.companyUsername);
    console.log('Password:', this.companyPassword);
  }

}
