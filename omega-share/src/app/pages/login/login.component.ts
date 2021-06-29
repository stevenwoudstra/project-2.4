import { getLocaleDateFormat } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../_services/auth.service';
import { TokenStorageService } from '../../_services/token-storage.service';


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  form: any = {
    username: null,
    password: null
   };

  isLoggedIn = false;
  isLoginFailed = false;
  id = null
  errorMessage = '';
  roles: string[] = [];

  constructor(private authService: AuthService, private tokenStorage: TokenStorageService, private router: Router) { }

  ngOnInit(): void {    
    if (this.tokenStorage.getToken()) {
      this.isLoggedIn = true;
      this.roles = this.tokenStorage.getUser().roles;
    }
  }
  
  ngAfterViewInit(): void {
    if(this.router.url == "/login/1") {
      document.getElementById("form-signin")?.classList.remove("omega-fade-in");
    } else {
      document.getElementById("input-fields-1")!.outerHTML = "";
      document.getElementById("input-fields-2")!.outerHTML = "";
      document.getElementById("buttons")?.classList.remove("buttons-login");
    }
  }

  onSubmit(): void {
    const { username, password } = this.form;
    console.log("kaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaas");
    this.authService.login(username, password).subscribe(
      data => {
        this.tokenStorage.saveToken(data.access_token);
        console.log(data.access_token);
        this.id= data.user.id

        this.isLoginFailed = false;
        this.isLoggedIn = true;
        this.getData();
      },
      err => {
        this.errorMessage = err.error.message;
        this.isLoginFailed = true;
      }
    );
  }
  getData(): void {
    this.authService.afterLogin().subscribe(
      data => {
        this.tokenStorage.saveUser(data.user);
        this.isLoginFailed = false;
        this.isLoggedIn = true;
        this.roles = this.tokenStorage.getUser().roles;
              
        // this.reloadPage();
        this.authService.isUserLoggedIn.next(true);
        this.router.navigate(['/profile']);
      },
      err => {
        this.errorMessage = err.error.message;
        this.isLoginFailed = true;
        this.tokenStorage.signOut()
        // this.reloadPage();
      }
    );
  }

  

  reloadPage(): void {
    window.location.reload();
  }

}
