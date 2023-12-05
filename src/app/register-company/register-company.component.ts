import { Component,OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { EncDecService } from '../encdec.service';
import { FormControl, Validators } from '@angular/forms';

@Component({
  selector: 'app-register-company',
  templateUrl: './register-company.component.html',
  styleUrls: ['./register-company.component.css']
})
export class RegisterCompanyComponent implements OnInit {

  constructor(
    private http:HttpClient, 
    private toastr: ToastrService, 
    private router: Router,
    private EncrDecr: EncDecService,
    )
  {
    obj:String;
  }
    ngOnInit(): void
    {
     
    }
  
page = 1; // Current page
  formData: any = {}; // Data object to store form values

  nextPage() {
    if (this.page === 1) {
      if (!this.companyName || !this.companyType) {
        this.toastr.error('Please fill in all required fields before proceeding to the next page.', 'Registration Failed', {
          positionClass: 'toast-top-center',
        });
        return;
      }
    } else if (this.page === 2) {
      if (!this.phone || !this.email) {
        this.toastr.error('Please fill in all required fields before proceeding to the next page.', 'Registration Failed', {
          positionClass: 'toast-top-center',
        });
        return;
      }
    } else if (this.page === 3) {
      if (!this.profile || !this.website || !this.licenseNo || !this.businessLicenseFile) {
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

  companyNameControl = new FormControl('', [
    Validators.required,
    Validators.minLength(3),
    Validators.maxLength(50),
    Validators.pattern('[a-zA-Z ]*')
  ]);
  phoneControl = new FormControl('', [
    Validators.required,
    Validators.pattern(/^\d{10}$/) // Adjust the pattern based on your requirements
  ]);
  emailControl = new FormControl('', [
    Validators.required,
    Validators.email
  ]);
  licenseNoControl = new FormControl('', [
    Validators.required,
    Validators.pattern('^[0-9]{10}$'), // Regular expression for a 10-character alphanumeric license number
  ]);

  companyPasswordControl = new FormControl('', [
    Validators.required,
    this.passwordValidator(),
  ]);

  onFileSelected(event: any) {
    this.businessLicenseFile = event.target.files[0];
  }

  onSubmit() {
    if (!this.companyPassword || !this.confirm_companyPassword) {
      this.toastr.error('Please fill in all required fields before submitting the form.', 'Registration Failed', {
        positionClass: 'toast-top-center',
      });
      return;
    }
    if (this.confirm_companyPassword !== this.companyPassword) {
      this.toastr.error('Passwords do not match', 'Validation Error', {
        positionClass: 'toast-top-center',
      });
      return;
    }
    var token = '123456$#@$^@1ERF'
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
    formData.append('confirm_companyPassword', this.EncrDecr.set(token, this.confirm_companyPassword));
    formData.append('company_password', this.EncrDecr.set(token, this.companyPassword));

    // Add the business license file, if selected
    if (this.businessLicenseFile) {
      formData.append('business_license', this.businessLicenseFile, this.businessLicenseFile.name);
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
