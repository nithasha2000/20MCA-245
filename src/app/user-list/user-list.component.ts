import { Component, OnInit } from '@angular/core';
import { ToastrService } from 'ngx-toastr';
import { UserService } from '../user.service';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-user-list',
  templateUrl: './user-list.component.html',
  styleUrls: ['./user-list.component.css']
})
export class UserListComponent implements OnInit {
  userData: any;
  users: any[] = [];

  constructor(
    private http: HttpClient,
    private toastr: ToastrService,
    private userService: UserService,
    private router: Router
  ) {}

  ngOnInit() {
    this.userData = this.userService.getUserData();

    if (this.userData) {
      const payload = {
        username: this.userData.username,
        role: this.userData.role
      };

      this.http.post('http://127.0.0.1:8000/view-users/', payload).subscribe((response: any) => {
      try {
        if (response.message === 'success') {
          this.users = response.data
        } 
        else if(response.data === 'Your are not authorized to view this page'){
          this.router.navigate(['/dashboard']);
          window.location.reload();
        }
        else {
          this.toastr.error(response.data, 'Failed to fetch users', {
            positionClass: 'toast-top-center',
          });
        }
      } catch (error) {
        this.toastr.error('Failed to fetch users', 'Try Again',{
          positionClass: 'toast-top-center',
        });
      }
    });
    }
  }

  viewUser(user: any) {
    console.log(user);
  }

  toggleUserActivation(user: any) {
    let payload = {
      "username": this.userData.username,
      "role": this.userData.role,
      "change_username": user.email
    }
    this.http.post('http://127.0.0.1:8000/account_activation/', payload).subscribe((response: any) => {
      try {
        if (response.message === 'success') {
          window.location.reload();
        } else {
          this.toastr.error(response.data, 'Failed to fetch users', {
            positionClass: 'toast-top-center',
          });
        }
      } catch (error) {
        this.toastr.error('Failed to fetch users', 'Try Again',{
          positionClass: 'toast-top-center',
        });
      }
    });
    }
}
