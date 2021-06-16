import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'omega-share';
  isAuthenticated: boolean;

  constructor() {
    this.isAuthenticated = false;
  }

  ngOnInit() {
    document.getElementById("bg")!.style.backgroundImage =
      [
        'url("/assets/img/backgrounds/000.png"',
        'url("/assets/img/backgrounds/001.png"',
        'url("/assets/img/backgrounds/002.png"',
        'url("/assets/img/backgrounds/003.png"',
        'url("/assets/img/backgrounds/004.png"',
        'url("/assets/img/backgrounds/005.png"',
        'url("/assets/img/backgrounds/006.png"',
        'url("/assets/img/backgrounds/007.png"',
        'url("/assets/img/backgrounds/008.png"',
        'url("/assets/img/backgrounds/009.png"'
      ][Math.floor(Math.random() * 10)];
  }

  login() {
  }

  logout() {
  }
}
