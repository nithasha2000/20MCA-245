import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HeaderComponent } from './header/header.component';
import { WorkComponent } from './work/work.component';
import { FooterComponent } from './footer/footer.component';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { RegisterCompanyComponent } from './register-company/register-company.component';
import { JobSeekerRegisterComponent } from './job-seeker-register/job-seeker-register.component';
import { AppLayoutComponent } from './app-layout/app-layout.component';
import { RegisterJobSeekerComponent } from './register-job-seeker/register-job-seeker.component';
import { HttpClientModule } from '@angular/common/http'
@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    FooterComponent,
    WorkComponent,
    LoginComponent,
    RegisterComponent,
    RegisterCompanyComponent,
    RegisterJobSeekerComponent,
    AppLayoutComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
