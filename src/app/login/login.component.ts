import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
})


export class LoginComponent {

  username: string = "";
  password: string = "";

  constructor(private http: HttpClient){

  }

  login(){

    let payload = {
      "username": this.username,
      "password": this.password
    };

    this.http.post("http://127.0.0.1:8000/login/", payload).subscribe((response: any)=>{
      console.log(response);
      alert("Login Successful")
    });
  }

}
