import { Component } from '@angular/core';
import { UserService } from '../user.service';
import { SocialAuthService, GoogleLoginProvider } from '@abacritt/angularx-social-login';
import { HttpClient } from '@angular/common/http';
import { ToastrService } from 'ngx-toastr';
import { Router } from '@angular/router';
import { CookieService } from 'ngx-cookie-service';

@Component({
  selector: 'app-header-dashboard',
  templateUrl: './header-dashboard.component.html',
  styleUrls: ['./header-dashboard.component.css']
})
export class HeaderDashboardComponent {
  // In your component class
  notificationCount: number = 5; // Replace with the actual number of notifications
  // In your component class
  // Call this method when there are new notifications
  updateNotificationCount(newCount: number) {
    this.notificationCount = newCount;
  }

  userData: any;
  isLoggingOut: boolean = false;
  constructor(private http: HttpClient, private toastr: ToastrService, 
    private authService: SocialAuthService, private userService: UserService, 
    private router: Router, private cookieService: CookieService) {
    this.userData = this.userService.getUserData();
    if (!this.userData){
      this.toastr.error('You are not authorized to view this page', 'Please Sign in', {
        positionClass: 'toast-top-center',
      });
      this.router.navigate(['/login']);
    }
  }
  logout() {
    if (this.isLoggingOut) {
      return;
    }
    this.isLoggingOut = true;
    if (this.userData.type == 'google'){
      if (this.authService.authState) {
        this.http.post('http://127.0.0.1:8000/logout/', this.userData).subscribe((response: any) => {
        try {
          if (response.message === 'success') {
            this.authService.signOut().then(() => {
              this.toastr.success('Logged Out', '', {
                positionClass: 'toast-top-center',
              });
              this.cookieService.delete('ability');
              this.userService.removeUserData();
              this.router.navigate(['/login']);
            }).catch((error) => {
              this.toastr.error('Failed to logout', '', {
                positionClass: 'toast-top-center',
              });
              console.error('Error during sign-out:', error);
            });
          } else {
            this.toastr.error(response.data, 'Logout Failed', {
              positionClass: 'toast-top-center',
            });
          }
        } catch (error) {
          this.toastr.error('Logout Failed', 'Try Again',{
            positionClass: 'toast-top-center',
          });
        }
      });
      } else {
        this.toastr.info('User is not logged in', '', {
          positionClass: 'toast-top-center',
        });
      }
    }
    else{  
      this.http.post('http://127.0.0.1:8000/logout/', this.userData).subscribe((response: any) => {
        try {
          if (response.message === 'success') {
            this.toastr.success('Logged Out', 'Logout Successful', {
              positionClass: 'toast-top-center',
            });
            this.cookieService.delete('ability');
            this.userService.removeUserData();
            this.router.navigate(['/login']);
          } else {
            this.toastr.error(response.data, 'Logout Failed', {
              positionClass: 'toast-top-center',
            });
          }
        } catch (error) {
          this.toastr.error('Logout Failed', 'Try Again',{
            positionClass: 'toast-top-center',
          });
        }
      });
    }
  }
}
