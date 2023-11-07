import { Component,OnInit, ViewChild } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { NgModel } from '@angular/forms';

@Component({
  selector: 'app-register-company',
  templateUrl: './register-company.component.html',
  styleUrls: ['./register-company.component.css']
})
export class RegisterCompanyComponent implements OnInit {

  //companyNameInput: NgModel | undefined;
  constructor(private http:HttpClient, private toastr: ToastrService, private router: Router)
  {
    obj:String;
  }
    ngOnInit(): void
    {
     
    }
  
page: number = 1; // Current page
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
  // streetAddressLine1!: string;
  // streetAddressLine2!: string;
  // city!: string;
  // state!: string;
  phone!: string;
  email!: string;
  profile!: string;
  website!: string;
  licenseNo!: string;
  businessLicenseFile: File | null = null; // This should be of type File if you plan to upload a file
  confirm_companyPassword!: string;
  companyPassword!: string;

   onFileSelected(event: any) {
    this.businessLicenseFile = event.target.files[0];
  }

  onSubmit() {
    const formData = new FormData();

    // Add form data fields
    formData.append('type', 'company_register');
    formData.append('company_name', this.companyName);
    formData.append('company_type', this.companyType);
    formData.append('phone', this.phone);
    formData.append('email', this.email);
    formData.append('profile', this.profile);
    formData.append('website', this.website);
    formData.append('license_no', this.licenseNo);
    formData.append('confirm_companyPassword', this.confirm_companyPassword);
    formData.append('company_password', this.companyPassword);

    // Add the business license file, if selected
    if (this.businessLicenseFile) {
      formData.append('business_license', this.businessLicenseFile, this.businessLicenseFile.name);
    }
    this.http.post('http://127.0.0.1:8000/register/', formData).subscribe((response: any) => {
      try {
        if (response.message === 'success') {
          this.toastr.success('Registered', 'Registration Successful', {
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
