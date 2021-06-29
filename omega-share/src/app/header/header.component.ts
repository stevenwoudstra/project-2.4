import { Component, OnInit } from '@angular/core';
import { ActivatedRouteSnapshot, Router } from '@angular/router';
import { AppComponent } from '../app.component';
import { AuthService } from '../_services/auth.service';
import { TokenStorageService } from './../_services/token-storage.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {
  isLoggedIn = false;

  username: any;
  profilePicture: string = "assets/placeholder pictures/stock_profile_picture.png";

  constructor(private tokenStorageService: TokenStorageService, private authService: AuthService, private router: Router) {
    router.events.subscribe((val) => {
      this.closeMobileNavbar();
  });
  }
  
  ngOnInit(): void {
    
        this.authService.isUserLoggedIn.subscribe(value => {
          this.isLoggedIn = value;
          const user = this.tokenStorageService.getUser();
          this.username = user.username;
        });
    // this.isLoggedIn = !!this.tokenStorageService.getToken();

    document.body.addEventListener('click', event => {
      if(!event.composedPath().includes(document.getElementById("app-header")!)) {
        this.closeMobileNavbar();
      }
    });
    document.body.addEventListener('touchstart', event => {
      if(!event.composedPath().includes(document.getElementById("app-header")!)) {
        this.closeMobileNavbar();
      }
    });

  }
  
  closeMobileNavbar(): void {
    if(document.getElementById("collapse_target")?.classList.contains("show")) {
      document.getElementById("navbar-btn")?.click();
    }
  }
  

  logout(): void {
    this.tokenStorageService.signOut();
    this.authService.isUserLoggedIn.next(false);
    this.router.navigate(['/home']);
  }

}
