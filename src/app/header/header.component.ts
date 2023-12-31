import { Component } from '@angular/core';
import { Router } from '@angular/router'

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})

export class HeaderComponent {
constructor(private router : Router) {}

handleLoginClick()
{
  this.router.navigate(['/login']);
}
handleCompanyRegisterClick()
{
  this.router.navigate(['/register-company']);
}
handleJobSeekerRegisterClick()
{
  this.router.navigate(['/register-job-seeker']);
}


}
