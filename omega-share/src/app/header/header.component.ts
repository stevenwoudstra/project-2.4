import { Component, OnInit } from '@angular/core';
import { AppComponent } from '../app.component';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
  }

  navbarClick() {
    if(window.matchMedia("(max-width: 575px)").matches) {
      document.getElementById("navbar-btn")?.click();
    }
  }

}
