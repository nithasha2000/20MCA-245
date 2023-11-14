import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { ToastrService } from 'ngx-toastr';
import { UserService } from '../user.service';
import { Router } from '@angular/router';
import { CookieService } from 'ngx-cookie-service';


@Component({
  selector: 'app-forgot-password',
  templateUrl: './forgot-password.component.html',
  styleUrls: ['./forgot-password.component.css']
})
export class ForgotPasswordComponent {
   email!: string
  ViewOtp!: string
  otp!: string
  constructor(private http: HttpClient, 
    private toastr: ToastrService, 
    private router: Router, 
    private userService: UserService,
    private cookieService: CookieService) {
  }
  send_email(){
    let payload = {
      "email": this.email
    }
    this.http.post('http://127.0.0.1:8000/forgot-password/', payload).subscribe((response: any) => {
      try {
        if (response.message === 'success') {
          this.toastr.success('An mail has been send to your registered email address', "Email Verification", {
            positionClass: 'toast-top-center',
          });
          this.ViewOtp = "view"
        } else {
          this.toastr.error(response.data, 'Change Password Failed', {
            positionClass: 'toast-top-center',
          });
        }
      } catch (error) {
        this.toastr.error('Change Password Failed', 'Try Again',{
          positionClass: 'toast-top-center',
        });
      }
    });
  }
  verify_otp(){
    let payload = {
      "email": this.email,
      "otp": this.otp
    }
    this.http.post('http://127.0.0.1:8000/verify-otp/', payload).subscribe((response: any) => {
      try {
        if (response.message === 'success') {
          this.ViewOtp = ""
          this.userService.setForgotPassword(response.data)
          this.router.navigate(['/change-password'])
        } else {
          this.toastr.error(response.data, 'Change Password Failed', {
            positionClass: 'toast-top-center',
          });
        }
      } catch (error) {
        this.toastr.error('Change Password Failed', 'Try Again',{
          positionClass: 'toast-top-center',
        });
      }
    });
  }
}
