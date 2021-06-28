import { Component, OnInit } from '@angular/core';
import { AppComponent } from '../app.component';
import { DataSharingService } from '../_services/data-sharing.service';
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

  constructor(private tokenStorageService: TokenStorageService, private dataSharingService: DataSharingService) { }
  
  ngOnInit(): void {
    
        this.dataSharingService.isUserLoggedIn.subscribe(value => {
          this.isLoggedIn = value;
          const user = this.tokenStorageService.getUser();
          this.username = user.username;

        });
    // this.isLoggedIn = !!this.tokenStorageService.getToken();
  }

  navbarClick() {
    if (window.matchMedia("(max-width: 575px)").matches) {
      document.getElementById("navbar-btn")?.click();
    }
  }
  logout(): void {
    this.tokenStorageService.signOut();
    window.location.reload();
  }

}
