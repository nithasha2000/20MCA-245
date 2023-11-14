import { HttpClient } from '@angular/common/http';
import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { ToastrService } from 'ngx-toastr';
import { UserService } from '../user.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.css']
})
export class SidebarComponent implements OnInit{
  userData: any;
  navItems: any[] = [];
  constructor(private http: HttpClient, 
    private toastr: ToastrService, 
    private userService: UserService, 
    private router: Router) {
      this.userData = this.userService.getUserData();
  }
  ngOnInit(){
    let payload = {
      "email": this.userData.username,
      "role": this.userData.role
    }
    this.http.post('http://127.0.0.1:8000/dashboard-sidebar/', payload).subscribe((response: any) => {
      try {
        if (response.message === 'success') {
          this.navItems = response.data
        } else {
          this.toastr.error(response.data, 'Side bar load failed', {
            positionClass: 'toast-top-center',
          });
        }
      } catch (error) {
        this.toastr.error('Side bar load failed', 'Try Again',{
          positionClass: 'toast-top-center',
        });
      }
    });
  }
  @Output() featureSelected = new EventEmitter<String>();
  onSelect(feature: string){
    this.featureSelected.emit(feature);
  }
}

