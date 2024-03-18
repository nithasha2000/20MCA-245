import { Component, ElementRef, OnInit, ViewChild, AfterViewInit, HostListener } from '@angular/core';
import { Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { UserService } from '../user.service';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-exam',
  templateUrl: './exam.component.html',
  styleUrls: ['./exam.component.css']
})
export class ExamComponent implements OnInit, AfterViewInit  {
  @ViewChild('examContainer') examContainer!: ElementRef;
  questions: any[] = [];
  userData: any;
  exam_create_id: any;
  exams: any = [];
  timer: any;
  timeLeft: number = 0;
  timeoutPopupVisible: boolean = false;
  timeremainingPopupVisible: boolean = false;
  examSubmitted: boolean = false;

  constructor(
    private http: HttpClient,
    private router: Router, 
    private toastr: ToastrService, 
    private userService: UserService
  ) {}

  ngOnInit() {
    this.userData = this.userService.getUserData();
    if(!this.userData){
      this.toastr.warning("Please login before continuing", 'Login Required', {
        positionClass: 'toast-top-center',
      });
      this.userService.setExamClick();
      this.router.navigate(['/login']);
      return;
    }

    this.exams = this.userService.getExamAttend();
    if (!this.exams) {
      this.toastr.warning("Please select an exam", 'Exam is required', {
        positionClass: 'toast-top-center',
      });
      this.router.navigate(['/exam-widget']);
      return;
    }

    if (this.exams.agreement === "false") {
      this.toastr.warning("Please agree to the instructions", 'Agreement Required', {
        positionClass: 'toast-top-center',
      });
      this.router.navigate(['/exam-instruction']);
      return;
    }

    if (!this.exams.exam_create_id) {
      this.toastr.warning("Please select an exam", 'Exam is required', {
        positionClass: 'toast-top-center',
      });
      this.router.navigate(['/exam-widget']);
      return;
    }

    this.exam_create_id = this.exams.exam_create_id;

    this.timeLeft = this.exams.duration * 60;
    this.startTimer();
    this.retrieveExamQuestion();
  }

  ngAfterViewInit() {
    this.enterFullscreen();
    document.addEventListener('keydown', this.preventEscapeKey.bind(this));
  }

  enterFullscreen() {
    const elem = this.examContainer.nativeElement;
    if (elem.requestFullscreen) {
      elem.requestFullscreen();
    } else if (elem.webkitRequestFullscreen) { /* Safari */
      elem.webkitRequestFullscreen();
    } else if (elem.msRequestFullscreen) { /* IE11 */
      elem.msRequestFullscreen();
    }

    document.addEventListener('fullscreenchange', this.preventExitFullscreen.bind(this));
    document.addEventListener('webkitfullscreenchange', this.preventExitFullscreen.bind(this));
    document.addEventListener('mozfullscreenchange', this.preventExitFullscreen.bind(this));
    document.addEventListener('MSFullscreenChange', this.preventExitFullscreen.bind(this));
    const fullscreenElement = document.fullscreenElement;
    fullscreenElement?.addEventListener('keydown', this.preventExitFullscreen.bind(this));
  }

  preventExitFullscreen(event: Event) {
    if (!document.fullscreenElement) {
      event.preventDefault();
    }
  }


  preventEscapeKey(event: KeyboardEvent) {
    console.log(event)
    if (event.key === 'Escape') {
      event.preventDefault();
    }
  }
  
  startTimer() {
    this.timer = setInterval(() => {
      this.timeLeft--;
      const timerElement = document.getElementById('timer');
      if (timerElement) {
        const minutes = Math.floor(this.timeLeft / 60);
        const seconds = this.timeLeft % 60;
        timerElement.innerText = `${minutes}:${seconds < 10 ? '0' + seconds : seconds}`;
      }
      if (this.timeLeft <= 0) {
        clearInterval(this.timer);
        this.showTimeoutPopup();
        this.submitExam();
      }
    }, 1000);
  }

  showTimeoutPopup() {
    this.timeoutPopupVisible = true;
  }

  hideTimeoutPopup() {
    this.timeoutPopupVisible = false;
  }

  showTimeRemainingPopup() {
    this.timeremainingPopupVisible = true;
  }

  hideTimeRemainingPopup() {
    this.timeremainingPopupVisible = false;
  }

  getOptionLetter(index: number): string {
    return String.fromCharCode(65 + index); // A: 65, B: 66, C: 67, etc.
  }

  retrieveExamQuestion() {
    const formData = {
      "username": this.userData.username,
      "role": this.userData.role,
      "exam_create_id": this.exam_create_id
    };
    
    this.http.post('http://127.0.0.1:8000/attend-exam-fetch/', formData).subscribe((response: any) => {
      try {
        if (response.message === 'success') {
          this.questions = response.data.questions;
        } else {
          this.toastr.error(response.data, 'Fetching Failed', {
            positionClass: 'toast-top-center',
          });
        }
      } catch (error) {
        this.toastr.error('Fetching Failed', 'Try Again',{
          positionClass: 'toast-top-center',
        });
      }
    });
  }

  submitExam() {
    if (this.examSubmitted) {
      this.toastr.warning("Already Submitted", 'Exam Submitted', {
        positionClass: 'toast-top-center',
      });
      return;
  }
  this.examSubmitted = true;
    const formData = {
      "username": this.userData.username,
      "role": this.userData.role,
      "exam_create_id": this.exam_create_id,
      "time_left": this.timeLeft,
      "questions": this.questions.map(question => {
        let selectedOption = null; // Initialize selected option as null
        if (question.AnswerIndex !== undefined && question.AnswerIndex !== null) {
            selectedOption = this.getOptionLetter(question.AnswerIndex);
        }
        return {
            exam_id: question.exam_id,
            description: question.description,
            options: question.options.map((option: any) => option.text),
            AnswerIndex: selectedOption // Assign selected option or null
        };
    })
    };
    
    this.http.post('http://127.0.0.1:8000/submit-exam/', formData).subscribe((response: any) => {
      try {
        if (response.message === 'success') {
          this.toastr.success('Exam Submitted', "Exam Completed", {
            positionClass: 'toast-top-center',
          });
          setTimeout(() => {
            this.router.navigate(['/result']);
        }, 3000);
        } else {
          this.toastr.error(response.data, 'Submitting Exam Failed', {
            positionClass: 'toast-top-center',
          });
        }
      } catch (error) {
        this.toastr.error('Submitting Exam Failed', 'Try Again',{
          positionClass: 'toast-top-center',
        });
      }
    });
  }

}
