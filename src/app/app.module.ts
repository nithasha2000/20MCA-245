import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import {ToastrModule} from 'ngx-toastr';
import { GoogleSigninButtonModule, SocialLoginModule, SocialAuthServiceConfig } from '@abacritt/angularx-social-login';
import {
  GoogleLoginProvider
} from '@abacritt/angularx-social-login';


import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HeaderComponent } from './header/header.component';
import { WorkComponent } from './work/work.component';
import { FooterComponent } from './footer/footer.component';
import { LoginComponent } from './login/login.component';
import { RegisterCompanyComponent } from './register-company/register-company.component';
import { JobSeekerRegisterComponent } from './job-seeker-register/job-seeker-register.component';
import { RegisterJobSeekerComponent} from './register-job-seeker/register-job-seeker.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HeaderDashboardComponent } from './header-dashboard/header-dashboard.component';
import { SidebarComponent } from './sidebar/sidebar.component';
import { MainContentComponent } from './main-content/main-content.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { ChangePasswordComponent } from './change-password/change-password.component';
import { ForgotPasswordComponent } from './forgot-password/forgot-password.component';
import { UserListComponent } from './user-list/user-list.component';
import { UserDataComponent } from './user-data/user-data.component';
import { CapitalizePipe } from './pipe.component';
import { JobPostComponent } from './job-post/job-post.component';
import { CookieService } from 'ngx-cookie-service';
import { CompanyDashboardComponent } from './company-dashboard/company-dashboard.component';
import { CompanyHeaderDashboardComponent } from './company-header-dashboard/company-header-dashboard.component';
import { CompanySidebarComponent } from './company-sidebar/company-sidebar.component';
import { CompanyMaincontentComponent } from './company-maincontent/company-maincontent.component';
import { JobPostWidgetComponent } from './job-post-widget/job-post-widget.component';

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    WorkComponent,
    FooterComponent,
    LoginComponent,
    JobSeekerRegisterComponent,
    RegisterCompanyComponent,
    RegisterJobSeekerComponent,
    HeaderDashboardComponent,
    SidebarComponent,
    MainContentComponent,
    DashboardComponent,
    ChangePasswordComponent,
    ForgotPasswordComponent,
    UserListComponent,
    UserDataComponent,
    CapitalizePipe,
    JobPostComponent,
    CompanyDashboardComponent,
    CompanyHeaderDashboardComponent,
    CompanySidebarComponent,
    CompanyMaincontentComponent,
    JobPostWidgetComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    ReactiveFormsModule, 
    HttpClientModule,
    BrowserAnimationsModule,
    SocialLoginModule,
    GoogleSigninButtonModule,
    ToastrModule.forRoot({

    })
  ],
  providers: [
    {
      provide: 'SocialAuthServiceConfig',
      useValue: {
        autoLogin: false,
        providers: [
          {
            id: GoogleLoginProvider.PROVIDER_ID,
            provider: new GoogleLoginProvider(
              '873860161285-oinhstdgi1rg419l2afcv6na21c8an6o.apps.googleusercontent.com'
            )
          }
        ],
        onError: (err) => {
          console.error(err);
        }
      } as SocialAuthServiceConfig,
    },
    CookieService,
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }