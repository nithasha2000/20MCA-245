import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-exam',
  templateUrl: './exam.component.html',
  styleUrls: ['./exam.component.css']
})
export class ExamComponent implements OnInit {
  examTitle: string = 'Sample Exam';
  examDuration: number = 60; // in minutes
  questions: any[] = [
    { id: 1, text: 'What is 2 + 2?', options: ['3', '4', '5'], correctAnswer: '4' },
    // Add more questions here
  ];

  constructor() { }

  ngOnInit(): void {
  }
}
