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
  oldPassword: string = '';
  newPassword: string = '';
  confirmPassword: string = '';

  constructor(private http: HttpClient, private toastr: ToastrService, 
    private userService: UserService, 
    private router: Router, private cookieService: CookieService) {
      this.userData = this.userService.getUserData();
      if (this.userData.type == 'google'){
        this.toastr.error('Feature Not available', 'Google Login', {
            positionClass: 'toast-top-center',
          });
        this.router.navigate(['/dashboard']);
    }
  }
  change_password(){
    let payload = {
      "username": this.userData.username,
      "role": this.userData.role,
      "oldPassword": this.oldPassword,
      "newPassword": this.newPassword,
      "confirmPassword": this.confirmPassword
    }
    this.http.post('http://127.0.0.1:8000/change_password/', payload).subscribe((response: any) => {
      try {
        if (response.message === 'success') {
          this.toastr.success('Please login with new password', 'Password Changed', {
            positionClass: 'toast-top-center',
          });
          this.cookieService.delete('ability');
          this.userService.removeUserData();
          this.router.navigate(['/login']);
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
