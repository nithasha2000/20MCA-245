import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private storageKey = 'userData'; 
  private storageKeyForgot = 'forgotEmail'; 
  private storageKeyJobPost = 'jobPost'; 
  private storageKeyLastEmitted = 'lastEmitted'
  private isLoggingIn = false;
  private navItemEmitted = "";
  private exam_create_id ="";

  constructor() {
    // Check the user's authentication status when the service is initialized
    const storedData = localStorage.getItem(this.storageKey);
    this.isLoggingIn = storedData ? true : false;
  }

  isLoggedIn(): boolean {
    return this.isLoggingIn;
  }

  // forgot pass
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

  // job post
  setJobPost(data: any) {
    localStorage.setItem(this.storageKeyJobPost, JSON.stringify(data));
  }

  getJobPost() {
    const storedDataJob = localStorage.getItem(this.storageKeyJobPost);
    return storedDataJob ? JSON.parse(storedDataJob) : null;
  }

  removeJobPost() {
    localStorage.removeItem(this.storageKeyJobPost);
  }


  // user data
  setUserData(data: any) {
    localStorage.setItem(this.storageKey, JSON.stringify(data));
    this.isLoggingIn = true;
  }

  getUserData() {
    const storedData = localStorage.getItem(this.storageKey);
    return storedData ? JSON.parse(storedData) : null;
  }

  removeUserData() {
    localStorage.removeItem(this.storageKey);
    this.isLoggingIn = false;
  }

  //last emitted
  setLastEmittedData(data: any) {
    localStorage.setItem(this.storageKeyLastEmitted, data);
  }

  getLastEmittedData() {
    const storedData = localStorage.getItem(this.storageKeyLastEmitted);
    return storedData !== null ? storedData : null;
  }

  removeLastEmittedData() {
    localStorage.removeItem(this.storageKeyLastEmitted);
  }

  setNavItemData(data: any) {
    localStorage.setItem(this.navItemEmitted, data);
  }
  getNavItemData() {
    const storedNavData = localStorage.getItem(this.navItemEmitted);
    return storedNavData !== null ? storedNavData : null;
  }
  removeNavItemData() {
    localStorage.removeItem(this.navItemEmitted);
  }
  setExamCreateIdData(data: any) {
    localStorage.setItem(this.exam_create_id, data);
  }
  getExamCreateIdData() {
    const storedNavData = localStorage.getItem(this.exam_create_id);
    return storedNavData !== null ? storedNavData : null;
  }
  removeExamCreateIdData() {
    localStorage.removeItem(this.exam_create_id);
  }
}
