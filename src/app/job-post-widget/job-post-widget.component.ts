import { Component,Input } from '@angular/core';

@Component({
  selector: 'app-job-post-widget',
  templateUrl: './job-post-widget.component.html',
  styleUrls: ['./job-post-widget.component.css']
})
export class JobPostWidgetComponent {
  @Input() jobTitle: string = '';
  @Input() companyName: string = '';
  @Input() experience: string = '';
  @Input() salary: string = '';
  @Input() location: string = '';
  @Input() jobDescription: string = '';
  @Input() applicationDeadline: string = '';

}
