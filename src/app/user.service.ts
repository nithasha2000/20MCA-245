import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private storageKey = 'userData'; 

  private storageKeyForgot = 'forgotEmail'; 
  setForgotPassword(data: any){
    localStorage.setItem(this.storageKeyForgot, JSON.stringify(data));
  }
  getForgotPassword() {
    const storedDataForgot = localStorage.getItem(this.storageKeyForgot);
    return storedDataForgot ? JSON.parse(storedDataForgot) : null;
  }
  removeForgotPassword() {
    localStorage.removeItem(this.storageKeyForgot);
  }

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
