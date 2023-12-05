import { Component, EventEmitter, OnDestroy, OnInit, Output } from '@angular/core';
import { UserService } from '../user.service';
import { SocialAuthService } from '@abacritt/angularx-social-login';
import { HttpClient } from '@angular/common/http';
import { ToastrService } from 'ngx-toastr';
import { Router } from '@angular/router';
import { CookieService } from 'ngx-cookie-service';
import { ReloadService } from '../reload.service';

@Component({
  selector: 'app-header-dashboard',
  templateUrl: './header-dashboard.component.html',
  styleUrls: ['./header-dashboard.component.css']
})
export class HeaderDashboardComponent implements OnInit, OnDestroy  {

  private updateInterval: any;
  notifications: any[] = [];
  showNotificationBox: boolean = false;
  toggleNotificationBox() {
    this.showNotificationBox = !this.showNotificationBox;
  }

  @Output() featureSelected = new EventEmitter<String>();
  onSelect(feature: string){
    this.reloadService.triggerReload();
    this.featureSelected.emit(feature);
  }

  // In your component class
  notificationCount: number = 0; // Replace with the actual number of notifications
  // In your component class
  // Call this method when there are new notifications
  updateNotification() {
    var payload = {
      "username": this.userData.username,
      "role": this.userData.role,
    }
    this.http.post('http://127.0.0.1:8000/notifications/', payload).subscribe((response: any) => {
      try {
        if (response.message === 'success') {
          this.notifications = response.data
          this.notificationCount = response.count
        } 
        else {
          if (Array.isArray(response.data)) {
            response.data.forEach((item: any) => {
              this.toastr.error(item, 'Failed to fetch notifications', {
                positionClass: 'toast-top-center',
              });
            });
          } else {
            this.toastr.error(response.data, 'Failed to fetch notifications', {
              positionClass: 'toast-top-center',
            });
          }
        }
      } catch (error) {
        this.toastr.error('Failed to fetch notifications', 'Try Again',{
          positionClass: 'toast-top-center',
        });
      }
    });
  }

  ngOnInit(): void {
    this.updateNotification(); // Call it once on component initialization

    // Set up an interval to call updateNotification every second
    this.updateInterval = setInterval(() => {
      this.updateNotification();
    }, 1000);
  }

  ngOnDestroy() {
    // Clear the interval when the component is destroyed
    clearInterval(this.updateInterval);
  }

  markAsRead(notification: any) {
    console.log(notification)
    var payload = {
      "username": this.userData.username,
      "role": this.userData.role,
      "notification_id": notification.notification_id
    }
    this.http.post('http://127.0.0.1:8000/mark-notifications/', payload).subscribe((response: any) => {
      try {
        if (response.message === 'success') {
          this.toastr.success('Success', 'Marked as read',{
            positionClass: 'toast-top-center',
          });
        } 
        else {
          if (Array.isArray(response.data)) {
            response.data.forEach((item: any) => {
              this.toastr.error(item, 'Failed to mark notifications', {
                positionClass: 'toast-top-center',
              });
            });
          } else {
            this.toastr.error(response.data, 'Failed to mark notifications', {
              positionClass: 'toast-top-center',
            });
          }
        }
      } catch (error) {
        this.toastr.error('Failed to mark notifications', 'Try Again',{
          positionClass: 'toast-top-center',
        });
      }
    });
  }

  userData: any;
  isLoggingOut: boolean = false;
  constructor(
    private http: HttpClient, 
    private toastr: ToastrService, 
    private authService: SocialAuthService, 
    private userService: UserService, 
    private router: Router, 
    private cookieService: CookieService,
    private reloadService: ReloadService) {
      
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
              this.toastr.success('Logged Out', '', {
                positionClass: 'toast-top-center',
              });
              this.userService.removeUserData();
              this.router.navigate(['/login']);
              console.error('Error during sign-out:', error);
            });
          } else {
            this.toastr.error(response.data, 'Logout Failed', {
              positionClass: 'toast-top-center',
            });
            this.cookieService.delete('ability');
            this.userService.removeUserData();
            this.router.navigate(['/login']);

          }
        } catch (error) {
          this.toastr.error('Logout Failed', 'Try Again',{
            positionClass: 'toast-top-center',
          });
          this.cookieService.delete('ability');
          this.userService.removeUserData();
          this.router.navigate(['/login']);
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
            this.cookieService.delete('ability');
            this.userService.removeUserData();
            this.router.navigate(['/login']);
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
