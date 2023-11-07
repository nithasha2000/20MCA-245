import { Component } from '@angular/core';
import { SocialAuthService, GoogleLoginProvider } from '@abacritt/angularx-social-login';
import { HttpClient } from '@angular/common/http';
import { ToastrService } from 'ngx-toastr';
import { UserService } from '../user.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
})

export class LoginComponent {

  username: string = '';
  password: string = '';
  isLoggingIn: boolean = false;

  constructor(private http: HttpClient, private toastr: ToastrService, 
    private authService: SocialAuthService, private userService: UserService, 
    private router: Router) {
    this.authService.authState.subscribe((user: any) => {
      try{
          if (user) {
            if (this.isLoggingIn) {
              return;
            }
            this.isLoggingIn = true;
            let payload = {
                "type": "google",
                "access_token": user.idToken
            }
            this.http.post('http://127.0.0.1:8000/login/', payload).subscribe((response: any) => {
            try {
              if (response.message === 'success') {
                this.toastr.success('Logged In', 'Login Successful', {
                  positionClass: 'toast-top-center',
                });
                this.userService.setUserData(response.data);
                this.router.navigate(['/dashboard']);
              } else {
                this.isLoggingIn = false;
                this.toastr.error(response.data, 'Login Failed', {
                  positionClass: 'toast-top-center',
                });
              }
            } catch (error) {     
              this.isLoggingIn = false;
              this.toastr.error('Login Failed', 'Try Again',{
                positionClass: 'toast-top-center',
              });
            }
          });

          }
      }
      catch{
        this.isLoggingIn = false;
        this.toastr.error('Failed to Signin', '',{
          positionClass: 'toast-top-center',
        });
      }
    });
  }

  login() {
    if (this.isLoggingIn) {
      return;
    }
    this.isLoggingIn = true;
    let payload = {
      type: 'normal',
      username: this.username,
      password: this.password,
    };

    this.http.post('http://127.0.0.1:8000/login/', payload).subscribe((response: any) => {
      try {
        if (response.message === 'success') {
          this.toastr.success('Logged In', 'Login Successful', {
            positionClass: 'toast-top-center',
          });
          this.userService.setUserData(response.data);
          this.router.navigate(['/dashboard']);
        } else {
          this.isLoggingIn = false;
          this.toastr.error(response.data, 'Login Failed', {
            positionClass: 'toast-top-center',
          });
        }
      } catch (error) {
        this.isLoggingIn = false;
        this.toastr.error('Login Failed', 'Try Again',{
          positionClass: 'toast-top-center',
        });
      }
    });
  }
}
