import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-exam-widget',
  standalone: true,
  imports: [],
  templateUrl: './exam-widget.component.html',
  styleUrl: './exam-widget.component.css'
})
export class ExamWidgetComponent {
constructor(private router: Router){}

navigateToExam(){
this.router.navigate(['/exam'])}
}
