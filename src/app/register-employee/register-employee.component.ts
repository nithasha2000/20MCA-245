import { Component,OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { EncDecService } from '../encdec.service';
import { FormControl, Validators } from '@angular/forms';

@Component({
  selector: 'app-register-employee',
  templateUrl: './register-employee.component.html',
  styleUrls: ['./register-employee.component.css']
})
export class RegisterEmployeeComponent implements OnInit {

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


  submitForm() {
    // Handle form submission here
  }
  firstName!: string;
  lastName!: string;
  email!: string;
  confirm_employeePassword!: string;
  employeePassword!: string;

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

  emailControl = new FormControl('', [
    Validators.required,
    Validators.email
  ]);

  employeePasswordControl = new FormControl('', [
    Validators.required,
    this.passwordValidator(),
  ]);

  onSubmit() {
    if (!this.firstName || !this.lastName || !this.employeePassword || !this.confirm_employeePassword) {
      this.toastr.error('Please fill in all required fields before submitting the form.', 'Registration Failed', {
        positionClass: 'toast-top-center',
      });
      return;
    }
    if (this.confirm_employeePassword !== this.employeePassword) {
      this.toastr.error('Passwords do not match', 'Validation Error', {
        positionClass: 'toast-top-center',
      });
      return;
    }
    var token = '123456$#@$^@1ERF'
    const formData = new FormData();

    // Add form data fields
    formData.append('type', 'employee_register');
    formData.append('firstName', this.firstName);
    formData.append('lastName', this.lastName);
    formData.append('email', this.email);
    formData.append('confirm_employeePassword', this.EncrDecr.set(token, this.confirm_employeePassword));
    formData.append('employee_password', this.EncrDecr.set(token, this.employeePassword));

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
