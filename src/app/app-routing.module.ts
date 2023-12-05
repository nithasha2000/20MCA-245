import { Component, NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { HeaderComponent } from './header/header.component';
import { RegisterCompanyComponent } from './register-company/register-company.component';
import { RegisterJobSeekerComponent } from './register-job-seeker/register-job-seeker.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { ChangePasswordComponent } from './change-password/change-password.component';
import { ForgotPasswordComponent } from './forgot-password/forgot-password.component';
import { UserListComponent } from './user-list/user-list.component';
import { SidebarComponent } from './sidebar/sidebar.component';
import { JobPostComponent } from './job-post/job-post.component';
import { CompanyDashboardComponent } from './company-dashboard/company-dashboard.component';
import { CompanySidebarComponent } from './company-sidebar/company-sidebar.component';
import { JobPostWidgetComponent } from './job-post-widget/job-post-widget.component';
import { ApplyJobListComponent } from './apply-job-list/apply-job-list.component';
import { SaveJobListComponent } from './save-job-list/save-job-list.component';
import { ApplicantsListComponent } from './applicants-list/applicants-list.component';
import { AuthGuard } from './auth.guard';
import { ExamFormComponent } from './exam-form/exam-form.component';
import { ExamQuestionComponent } from './exam-question/exam-question.component';
import { RegisterEmployeeComponent } from './register-employee/register-employee.component';

const routes: Routes = [
{ path: '', component: HeaderComponent },
{ path: 'login', component: LoginComponent },
{ path: 'register-job-seeker', component: RegisterJobSeekerComponent },
{ path: 'register-company', component: RegisterCompanyComponent },
{ path: 'dashboard', component: DashboardComponent, canActivate: [AuthGuard]},
{ path: 'change-password', component: ChangePasswordComponent},
{ path: 'forgot-password', component: ForgotPasswordComponent},
{ path: 'view-users', component: UserListComponent},
{ path: 'job-post', component: JobPostComponent},
{ path: 'company-dashboard',component: CompanyDashboardComponent},
{ path: 'job-post-widget',component:JobPostWidgetComponent},
{ path: 'apply-job-list',component:ApplyJobListComponent},
{ path: 'save-job-list',component:SaveJobListComponent},
{ path: 'applicants-list',component:ApplicantsListComponent},
{ path: 'exam-form',component:ExamFormComponent},
{ path: 'exam-question',component:ExamQuestionComponent},
{ path: 'register-employee',component:RegisterEmployeeComponent},
];

const dashboardRoutes: Routes = [
  {
    path: 'dashboard',
    canActivate: [AuthGuard],
    component: DashboardComponent,
    children: [
      { path: 'change-password', component: ChangePasswordComponent },
      { path: 'forgot-password', component: ForgotPasswordComponent }
    ]
  }]

const sidebarRoutes: Routes = [
  {
    path: 'sidebar',
    component: SidebarComponent,
    children: [
      { path: 'view-users', component: UserListComponent}  
    ]
  }]

const companysidebarRoutes: Routes = [
  {
    path: 'company-sidebar',
    component: CompanySidebarComponent,
    children: [
      { path: 'job-post', component: JobPostComponent},
      { path: 'job-post-widget', component:JobPostWidgetComponent}
 ]
}]
@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }