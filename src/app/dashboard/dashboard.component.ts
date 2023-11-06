import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent {
constructor(private router: Router) {}

  navigateToPasswordChange(event: Event) {
    event.preventDefault(); 
    this.router.navigate(['dashboard', 'change-password']);
}
}