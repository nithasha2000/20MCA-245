import { HttpClient } from '@angular/common/http';
import { Component,EventEmitter,Input, OnInit, Output } from '@angular/core';
import { ToastrService } from 'ngx-toastr';
import { UserService } from '../user.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-job-post-widget',
  templateUrl: './job-post-widget.component.html',
  styleUrls: ['./job-post-widget.component.css']
})
export class JobPostWidgetComponent implements OnInit{
  job_list: any[] = [];
  userData: any;
  searchTerm: string = '';
  filterData = {
    job_title: '',
    soft_skills: '',
    location: '',
    salary_range: ''
  };

  onRefresh() {
    this.userService.setNavItemData("job-post-widget")
    this.userService.setLastEmittedData("job-post-widget");
    location.reload();
  }

  applyFilters() {
    const payload = {
      "username": this.userData.username,
      "role": this.userData.role,
      "search_value": this.searchTerm,
      "filterData": this.filterData
    };

    this.http.post('http://127.0.0.1:8000/job-post-filter/', payload).subscribe((response: any) => {
      try {
        if (response.message === 'success') {
          this.job_list = response.data
        } 
        else {
          if (Array.isArray(response.data)) {
            response.data.forEach((item: any) => {
              this.toastr.error(item, 'Job Post listing Failed', {
                  positionClass: 'toast-top-center',
                });
            });
          } else {
              this.toastr.error(response.data, 'Job Post listing Failed', {
                positionClass: 'toast-top-center',
              });
          }
        }
      } catch (error) {
        this.toastr.error('Job Post listing Failed', 'Try Again',{
            positionClass: 'toast-top-center',
          });
        }
    });
  }


  onSearchChange(searchTerm: string) {
    this.searchTerm = searchTerm;
    var filter_data = {
      "username": this.userData.username,
      "role": this.userData.role,
      "search_value": searchTerm,
      "filterData": this.filterData
    }
    this.http.post('http://127.0.0.1:8000/job-post-filter/', filter_data).subscribe((response: any) => {
      try {
        if (response.message === 'success') {
          this.job_list = response.data
        } 
        else {
          if (Array.isArray(response.data)) {
            response.data.forEach((item: any) => {
              this.toastr.error(item, 'Job Post listing Failed', {
                  positionClass: 'toast-top-center',
                });
            });
          } else {
              this.toastr.error(response.data, 'Job Post listing Failed', {
                positionClass: 'toast-top-center',
              });
          }
        }
      } catch (error) {
        this.toastr.error('Job Post listing Failed', 'Try Again',{
            positionClass: 'toast-top-center',
          });
        }
  });
  }

  constructor(
    private http: HttpClient,
    private toastr: ToastrService,
    private userService: UserService,
    private router: Router
  ) {}

  @Output() featureSelected = new EventEmitter<any>();
  onSelect(feature: string, job?: any) {
    if(job !== undefined){
      this.userService.setJobPost(job)
    }
    else{
      this.userService.removeJobPost()
    }
    this.featureSelected.emit(feature);
  }

  @Input() jobTitle: string = '';
  @Input() experience: string = '';
  @Input() salary: string = '';
  @Input() location: string = '';
  @Input() jobDescription: string = '';
  @Input() applicationDeadline: string = '';

  areButtonsVisible: { [key: string]: boolean } = {};

  toggleButtons(job: any) {
    // Set the visibility state for the specific job
    this.areButtonsVisible[job.job_post_id] = !this.areButtonsVisible[job.job_post_id];
    // Close buttons for other jobs
    Object.keys(this.areButtonsVisible).forEach(key => {
      if (key !== String(job.job_post_id)) {
        this.areButtonsVisible[key] = false;
      }
      else{
        this.areButtonsVisible[key] = true;
      }
    });
    // Add event listener to handle clicks outside the buttons area
    const clickHandler = (event: any) => {
      const clickedElement = event.target;
      const isButtonOrChild = this.isButtonOrChild(clickedElement);

      if (!isButtonOrChild) {
        // Clicked outside the buttons area, hide buttons
        this.areButtonsVisible[job.job_post_id] = false;
        document.removeEventListener('click', clickHandler);
      }
    };

    // Add the click event listener
    document.addEventListener('click', clickHandler);
  }

  // Helper function to check if the clicked element is the button or its child
  private isButtonOrChild(element: any): boolean {
    let currentElement = element;
    while (currentElement) {
      if (currentElement.classList && currentElement.classList.contains('toggle-buttons')) {
        return true;
      }
      currentElement = currentElement.parentNode;
    }
    return false;
  }
  getSoftSkillsList(softSkills: any): string[] {
    return Object.keys(softSkills).filter(skill => softSkills[skill]);
  }
  ngOnInit() {
    this.userData = this.userService.getUserData();

    if (this.userData) {
      const payload = {
        "username": this.userData.username,
        "role": this.userData.role
      };

      this.http.post('http://127.0.0.1:8000/view-job-list/', payload).subscribe((response: any) => {
      try {
        if (response.message === 'success') {
          this.job_list = response.data
        } 
        else if(response.data === 'Your are not authorized to view this page'){
          this.router.navigate(['/dashboard']);
          window.location.reload();
        }
        else {
          this.toastr.error(response.data, 'Failed to fetch view job list', {
            positionClass: 'toast-top-center',
          });
        }
      } catch (error) {
        this.toastr.error('Failed to fetch view job list', 'Try Again',{
          positionClass: 'toast-top-center',
        });
      }
    });
    }
  }

  onApply(job: any)
  {
    const payload = {
      "username": this.userData.username,
      "role": this.userData.role,
      "job_post_id": job.job_post_id
    };

    this.http.post('http://127.0.0.1:8000/apply-job/', payload).subscribe((response: any) => {
      try {
        if (response.message === 'success') {
          this.toastr.success('Job Applied', 'Applied for Job Successfully', {
              positionClass: 'toast-top-center',
            });
            this.userService.setNavItemData("apply-job-list")
            this.userService.setLastEmittedData("apply-job-list");
            location.reload();
        } 
        else {
          if (Array.isArray(response.data)) {
            response.data.forEach((item: any) => {
              this.toastr.error(item, 'Job Apply Failed', {
                  positionClass: 'toast-top-center',
                });
            });
          } else {
              this.toastr.error(response.data, 'Job Apply Failed', {
                positionClass: 'toast-top-center',
              });
          }
        }
      } catch (error) {
        this.toastr.error('Job Apply Failed', 'Try Again',{
            positionClass: 'toast-top-center',
          });
        }
  });
  }
  
  onSave(job: any)
  {
    const payload = {
      "username": this.userData.username,
      "role": this.userData.role,
      "job_post_id": job.job_post_id
    };

    this.http.post('http://127.0.0.1:8000/save-job/', payload).subscribe((response: any) => {
      try {
        if (response.message === 'success') {
          this.toastr.success('Job Saved', 'Job Saved Successfully', {
              positionClass: 'toast-top-center',
            });
            this.userService.setNavItemData("save-job-list")
            this.userService.setLastEmittedData("save-job-list");
            location.reload();
        } 
        else {
          if (Array.isArray(response.data)) {
            response.data.forEach((item: any) => {
              this.toastr.error(item, 'Job Save Failed', {
                  positionClass: 'toast-top-center',
                });
            });
          } else {
              this.toastr.error(response.data, 'Job Save Failed', {
                positionClass: 'toast-top-center',
              });
          }
        }
      } catch (error) {
        this.toastr.error('Job Save Failed', 'Try Again',{
            positionClass: 'toast-top-center',
          });
        }
  });
  }


  ondelete(job: any){
    const payload = {
      "type": "delete",
      "username": this.userData.username,
      "role": this.userData.role,
      "job_post_id": job.job_post_id
    };

    this.http.post('http://127.0.0.1:8000/job-post/', payload).subscribe((response: any) => {
      try {
        if (response.message === 'success') {
          this.toastr.success('Job Deleted', 'Job Deleted Successfully', {
              positionClass: 'toast-top-center',
            });
            this.userService.setNavItemData("job-post-widget")
            this.userService.setLastEmittedData("job-post-widget");
            location.reload();
        } 
        else {
          if (Array.isArray(response.data)) {
            response.data.forEach((item: any) => {
              this.toastr.error(item, 'Job Delete Failed', {
                  positionClass: 'toast-top-center',
                });
            });
          } else {
              this.toastr.error(response.data, 'Job Delete Failed', {
                positionClass: 'toast-top-center',
              });
          }
        }
      } catch (error) {
        this.toastr.error('Job Delete Failed', 'Try Again',{
            positionClass: 'toast-top-center',
          });
        }
  });
  }

  onstatus(job: any){
    const payload = {
      "type": "status",
      "username": this.userData.username,
      "role": this.userData.role,
      "job_post_id": job.job_post_id
    };

    this.http.post('http://127.0.0.1:8000/job-post/', payload).subscribe((response: any) => {
      try {
        if (response.message === 'success') {
          this.toastr.success('Job Status Changed', 'Job Status Changed Successfully', {
              positionClass: 'toast-top-center',
            });
            this.userService.setNavItemData("job-post-widget")
            this.userService.setLastEmittedData("job-post-widget");
            location.reload();
        } 
        else {
          if (Array.isArray(response.data)) {
            response.data.forEach((item: any) => {
              this.toastr.error(item, 'Job Status Change Failed', {
                  positionClass: 'toast-top-center',
                });
            });
          } else {
              this.toastr.error(response.data, 'Job Status Change Failed', {
                positionClass: 'toast-top-center',
              });
          }
        }
      } catch (error) {
        this.toastr.error('Job Status Change Failed', 'Try Again',{
            positionClass: 'toast-top-center',
          });
        }
  });
  }

  onApprove(job: any){
    const payload = {
      "type": "approval",
      "status": "approve",
      "username": this.userData.username,
      "role": this.userData.role,
      "job_post_id": job.job_post_id
    };

    this.http.post('http://127.0.0.1:8000/job-post-approve/', payload).subscribe((response: any) => {
      try {
        if (response.message === 'success') {
          this.toastr.success('Job Status Changed', 'Job Post Approved', {
              positionClass: 'toast-top-center',
            });
            this.userService.setNavItemData("job-post-widget")
            this.userService.setLastEmittedData("job-post-widget");
            location.reload();
        } 
        else {
          if (Array.isArray(response.data)) {
            response.data.forEach((item: any) => {
              this.toastr.error(item, 'Job Post Approval Failed', {
                  positionClass: 'toast-top-center',
                });
            });
          } else {
              this.toastr.error(response.data, 'Job Post Approval Failed', {
                positionClass: 'toast-top-center',
              });
          }
        }
      } catch (error) {
        this.toastr.error('Job Post Approval Failed', 'Try Again',{
            positionClass: 'toast-top-center',
          });
        }
  });
  }

  onReject(job: any){
    const payload = {
      "type": "approval",
      "status": "reject",
      "username": this.userData.username,
      "role": this.userData.role,
      "job_post_id": job.job_post_id
    };

    this.http.post('http://127.0.0.1:8000/job-post-approve/', payload).subscribe((response: any) => {
      try {
        if (response.message === 'success') {
          this.toastr.success('Job Post Status Changed', 'Job Post Rejected', {
              positionClass: 'toast-top-center',
            });
            this.userService.setNavItemData("job-post-widget")
            this.userService.setLastEmittedData("job-post-widget");
            location.reload();
        } 
        else {
          if (Array.isArray(response.data)) {
            response.data.forEach((item: any) => {
              this.toastr.error(item, 'Job Post Reject Failed', {
                  positionClass: 'toast-top-center',
                });
            });
          } else {
              this.toastr.error(response.data, 'Job Post Reject Failed', {
                positionClass: 'toast-top-center',
              });
          }
        }
      } catch (error) {
        this.toastr.error('Job Post Approval Failed', 'Try Again',{
            positionClass: 'toast-top-center',
          });
        }
  });
  }

}
