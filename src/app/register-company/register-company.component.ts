import { Component,OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-register-company',
  templateUrl: './register-company.component.html',
  styleUrls: ['./register-company.component.css']
})
export class RegisterCompanyComponent implements OnInit {

  constructor(private http:HttpClient)
  {
    obj:String;
  }
    ngOnInit(): void
    {
     
    }
  
page = 1; // Current page
  formData: any = {}; // Data object to store form values

  nextPage() {
    this.page++;
  }

  previousPage() {
    this.page--;
  }

  submitForm() {
    // Handle form submission here
  }
  companyName: string = '';
  companyType: string = '';
  streetAddressLine1!: string;
  streetAddressLine2!: string;
  city!: string;
  state!: string;
  phone!: string;
  email!: string;
  profile!: string;
  website!: string;
  licenseNo!: string;
  businessLicense!: File; // This should be of type File if you plan to upload a file
  companyUsername!: string;
  companyPassword!: string;

  onSubmit() {
    // Implement company registration logic here
    console.log('Company Form submitted');
    console.log('Company Name:', this.companyName);
    console.log('Company Type:', this.companyType);
    console.log('Street Address Line 1:', this.streetAddressLine1);
    console.log('Street Address Line 2:', this.streetAddressLine2);
    console.log('City:', this.city);
    console.log('State:', this.state);
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
