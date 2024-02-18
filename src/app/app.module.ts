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
import { CapitalizePipe } from './pipe.component';
import { JobPostComponent } from './job-post/job-post.component';
import { CookieService } from 'ngx-cookie-service';
import { CompanyDashboardComponent } from './company-dashboard/company-dashboard.component';
import { CompanyHeaderDashboardComponent } from './company-header-dashboard/company-header-dashboard.component';
import { CompanySidebarComponent } from './company-sidebar/company-sidebar.component';
import { CompanyMaincontentComponent } from './company-maincontent/company-maincontent.component';
import { JobPostWidgetComponent } from './job-post-widget/job-post-widget.component';
import { AuthGuard } from './auth.guard';
import { UserDetailsComponent } from './user-details/user-details.component';
import { ApplyJobListComponent } from './apply-job-list/apply-job-list.component';
import { SaveJobListComponent } from './save-job-list/save-job-list.component';
import { ApplicantsListComponent } from './applicants-list/applicants-list.component';
import { ReloadService } from './reload.service';
import { ExamFormComponent } from './exam-form/exam-form.component';
import { EncDecService } from './encdec.service';
import { ExamQuestionComponent } from './exam-question/exam-question.component';
import { RegisterEmployeeComponent } from './register-employee/register-employee.component';
import { ExamTableComponent } from './exam-table/exam-table.component';

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
    CapitalizePipe,
    JobPostComponent,
    CompanyDashboardComponent,
    CompanyHeaderDashboardComponent,
    CompanySidebarComponent,
    CompanyMaincontentComponent,
    JobPostWidgetComponent,
    UserDetailsComponent,
    ApplyJobListComponent,
    SaveJobListComponent,
    ApplicantsListComponent,
    ExamFormComponent,
    ExamQuestionComponent,
    RegisterEmployeeComponent,
    ExamTableComponent
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
    AuthGuard,
    CookieService,
    ReloadService,
    EncDecService,
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }