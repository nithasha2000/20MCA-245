import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { CompanyRegisterComponent } from './company-register/company-register.component';
import { JobSeekerRegisterComponent } from './job-seeker-register/job-seeker-register.component';
import { HeaderComponent } from './header/header.component';

const routes: Routes = [
{ path: '', component: HeaderComponent },
{ path: 'login', component: LoginComponent },
{ path: 'register', component: RegisterComponent},
{ path: 'company-register', component: CompanyRegisterComponent},
{ path: 'job-seeker-register', component: JobSeekerRegisterComponent}];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }