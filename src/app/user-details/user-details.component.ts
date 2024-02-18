import { Component } from '@angular/core';

@Component({
  selector: 'app-user-details',
  templateUrl: './user-details.component.html',
  styleUrls: ['./user-details.component.css']
})
export class UserDetailsComponent {
  users: any[] = []; // Define the users array property

  // Define the toggleUserActivation method
  toggleUserActivation(user: any) {
    // Implement the logic to toggle user activation
    console.log('Toggling user activation:', user);
  }
}