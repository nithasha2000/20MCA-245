import { Component, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-job-post-widget',
  templateUrl: './job-post-widget.component.html',
  styleUrls: ['./job-post-widget.component.css'],
})
export class JobPostWidgetComponent {
  @Input() jobTitle: string = '';
  @Input() companyName: string = '';
  @Input() experience: string = '';
  @Input() salary: string = '';
  @Input() location: string = '';
  @Input() jobDescription: string = '';
  @Input() applicationDeadline: string = '';

  areButtonsVisible = false;

  showButtons() {
    if (this.areButtonsVisible) {
      this.areButtonsVisible = false;
    }
  }

  toggleButtons() {
    this.areButtonsVisible = !this.areButtonsVisible;
  }
}
