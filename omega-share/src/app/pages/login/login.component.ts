import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  logOrReg: string = "log";

  constructor() { }

  ngOnInit(): void {

  }

  toggle(): void {
    if (this.logOrReg == "log") this.logOrReg = "reg"; else this.logOrReg = "log";
    console.log(this.logOrReg);
  }

}
