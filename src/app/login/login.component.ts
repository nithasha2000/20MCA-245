import { Component } from '@angular/core';
import { SocialAuthService, GoogleLoginProvider } from '@abacritt/angularx-social-login';
import { HttpClient } from '@angular/common/http';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
})

export class LoginComponent {

  username: string = '';
  password: string = '';
  private accessToken = '';

  constructor(private http: HttpClient, private toastr: ToastrService, private authService: SocialAuthService) {
    this.authService.authState.subscribe((user: any) => {
      try{
          if (user) {
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
              } else {
                this.toastr.error(response.data, 'Login Failed', {
                  positionClass: 'toast-top-center',
                });
              }
            } catch (error) {
              this.toastr.error('Login Failed', 'Try Again',{
                positionClass: 'toast-top-center',
              });
            }
          });

          }
      }
      catch{
        this.toastr.error('Failed to Signin', '',{
          positionClass: 'toast-top-center',
        });
      }
    });
  }

  login() {
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
        } else {
          this.toastr.error(response.data, 'Login Failed', {
            positionClass: 'toast-top-center',
          });
        }
      } catch (error) {
        this.toastr.error('Login Failed', 'Try Again',{
          positionClass: 'toast-top-center',
        });
      }
    });
  }

  logout() {
    if (this.authService.authState) {
      this.authService.signOut().then(() => {
        this.toastr.success('Logged Out', '', {
          positionClass: 'toast-top-center',
        });
      }).catch((error) => {
        this.toastr.error('Failed to logout', '', {
          positionClass: 'toast-top-center',
        });
        console.error('Error during sign-out:', error);
      });
    } else {
      this.toastr.info('User is not logged in', '', {
        positionClass: 'toast-top-center',
      });
    }
  }
}
