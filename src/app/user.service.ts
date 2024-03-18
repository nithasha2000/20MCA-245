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
  private exam_data ="";
  private exam_click =  "false";
  private exam_attend = "";

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
  setExamData(data: any) {
    localStorage.setItem(this.exam_data, JSON.stringify(data));
  }
  getExamData() {
    const storedNavData = localStorage.getItem(this.exam_data);
    return storedNavData !== null ? JSON.parse(storedNavData) : null;
  }
  removeExamdData() {
    localStorage.removeItem(this.exam_data);
  }
  setExamClick() {
    localStorage.setItem(this.exam_click, 'true');
  }
  getExamClick() {
    const storedNavData = localStorage.getItem(this.exam_click);
    return storedNavData !== null ? storedNavData : null;
  }
  removeExamClick() {
    localStorage.setItem(this.exam_click, 'false');
  }
  setExamAttend(data: any) {
    localStorage.setItem(this.exam_attend, JSON.stringify(data));
  }
  getExamAttend() {
    const storedNavData = localStorage.getItem(this.exam_attend);
    return storedNavData !== null ? JSON.parse(storedNavData) : null;
  }
  removeExamAttend() {
    localStorage.removeItem(this.exam_attend);
  }
}
