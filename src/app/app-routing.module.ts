import { Component, NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { HeaderComponent } from './header/header.component';
import { RegisterCompanyComponent } from './register-company/register-company.component';
import { RegisterJobSeekerComponent } from './register-job-seeker/register-job-seeker.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { ChangePasswordComponent } from './change-password/change-password.component';
import { ForgotPasswordComponent } from './forgot-password/forgot-password.component';

const routes: Routes = [
{ path: '', component: HeaderComponent },
{ path: 'login', component: LoginComponent },
{ path: 'register-job-seeker', component: RegisterJobSeekerComponent },
{ path: 'register-company', component: RegisterCompanyComponent },
{ path: 'dashboard', component: DashboardComponent},
{ path: 'change-password', component: ChangePasswordComponent},
{ path: 'forgot-password', component: ForgotPasswordComponent}
];

const dashboardRoutes: Routes = [
  {
    path: 'dashboard',
    component: DashboardComponent,
    children: [
      { path: 'change-password', component: ChangePasswordComponent },
      { path: 'forgot-password', component: ForgotPasswordComponent }
    ]
  }]

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }