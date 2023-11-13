// notification.service.ts

import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class NotificationService {
  private notificationSubject = new Subject<string>();

  // Observable to subscribe to for notifications
  notification$ = this.notificationSubject.asObservable();

  // Method to send a notification
  sendNotification(message: string) {
    this.notificationSubject.next(message);
  }
}
