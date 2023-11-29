import { HttpClient } from '@angular/common/http';
import { Component, EventEmitter, OnInit, Output, OnDestroy } from '@angular/core';
import { ToastrService } from 'ngx-toastr';
import { UserService } from '../user.service';
import { Subscription } from 'rxjs';
import { ReloadService } from '../reload.service';

@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.css']
})
export class SidebarComponent implements OnInit, OnDestroy{
  userData: any;
  navItems: any[] = [];
  selectedNavItem: string | null = null;
  private reloadSubscription: Subscription;

  constructor(private http: HttpClient, 
    private toastr: ToastrService, 
    private userService: UserService,
    private reloadService: ReloadService) {
      this.reloadSubscription = this.reloadService.getReloadObservable().subscribe(() => {
        this.onSelect("")
      });
      this.userData = this.userService.getUserData();
  }

  ngOnDestroy() {
    this.reloadSubscription.unsubscribe();
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
    this.selectedNavItem = feature;
  }
}

