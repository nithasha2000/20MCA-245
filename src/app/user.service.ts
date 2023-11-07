import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private storageKey = 'userData'; 

  setUserData(data: any) {
    localStorage.setItem(this.storageKey, JSON.stringify(data));
  }

  getUserData() {
    const storedData = localStorage.getItem(this.storageKey);
    return storedData ? JSON.parse(storedData) : null;
  }

  removeUserData() {
    localStorage.removeItem(this.storageKey);
  }
}
