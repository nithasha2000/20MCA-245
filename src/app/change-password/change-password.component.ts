import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { ToastrService } from 'ngx-toastr';
import { UserService } from '../user.service';
import { Router } from '@angular/router';
import { CookieService } from 'ngx-cookie-service';

@Component({
  selector: 'app-change-password',
  templateUrl: './change-password.component.html',
  styleUrls: ['./change-password.component.css']
})
export class ChangePasswordComponent {
  userData: any;
  forgotData: any;
  oldPassword: string = '';
  newPassword: string = '';
  confirmPassword: string = '';

  constructor(private http: HttpClient, private toastr: ToastrService, 
    private userService: UserService, 
    private router: Router, private cookieService: CookieService) {
      this.userData = this.userService.getUserData();
      this.forgotData = this.userService.getForgotPassword();
      if(this.userData){
        if (this.userData.type == 'google'){
            this.router.navigate(['/dashboard']);
        }
    }
  }
  change_password(){
    let payload = {

    }
    if(this.forgotData){
      payload = {
        "username": this.forgotData.username,
        "role": this.forgotData.role,
        "type": "change-password",
        "newPassword": this.newPassword,
        "confirmPassword": this.confirmPassword
      }
    }
    else{
      payload = {
        "username": this.userData.username,
        "role": this.userData.role,
        "type": "forgot-password",
        "oldPassword": this.oldPassword,
        "newPassword": this.newPassword,
        "confirmPassword": this.confirmPassword
      }
    }
    this.http.post('http://127.0.0.1:8000/change_password/', payload).subscribe((response: any) => {
      try {
        if (response.message === 'success') {
          this.toastr.success('Please login with new password', 'Password Changed', {
            positionClass: 'toast-top-center',
          });
          this.cookieService.delete('ability');
          this.userService.removeUserData();
          this.userService.removeForgotPassword();
          this.router.navigate(['/login']);
        } 
        else {
          if (Array.isArray(response.data)) {
            response.data.forEach((item: any) => {
              this.toastr.error(item, 'Change Password Failed', {
                positionClass: 'toast-top-center',
              });
            });
          } else {
            this.toastr.error(response.data, 'Change Password Failed', {
              positionClass: 'toast-top-center',
            });
          }
        }
      } catch (error) {
        this.toastr.error('Change Password Failed', 'Try Again',{
          positionClass: 'toast-top-center',
        });
      }
    });
  }
}
