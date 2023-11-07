import { Component, OnInit } from '@angular/core';
import { ToastrService } from 'ngx-toastr';
import { UserService } from '../user.service';
import { HttpClient } from '@angular/common/http';

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
    private userService: UserService
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
          console.log(this.users)
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

  viewUser(user: any) {
    console.log(user);
  }

  deactivateUser(user: any) {
    console.log(user);
  }
}
