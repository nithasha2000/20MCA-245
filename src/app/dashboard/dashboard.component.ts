import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { UserService } from '../user.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent {
  selectedFeature!: any;
  constructor(
    private router: Router,
    private userService: UserService
    ) {
      if(this.userService.getLastEmittedData()){
        this.selectedFeature = this.userService.getLastEmittedData()
        this.userService.removeLastEmittedData()
      }
      else{
        this.selectedFeature = 'dashboard';
      }
    }

    navigateToPasswordChange(event: Event) {
      event.preventDefault(); 
      this.router.navigate(['dashboard', 'change-password']);
  }
  onNavigate(feature: any){
    this.selectedFeature = feature;
  }
}
