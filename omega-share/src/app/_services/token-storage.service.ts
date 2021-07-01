import { Injectable } from '@angular/core';
import { AuthService } from '../_services/auth.service';
import { Observable } from 'rxjs';


const TOKEN_KEY = 'auth-token';
const USER_KEY = 'auth-user';
const REFRESH_KEY = 'refresh-token';

@Injectable({
  providedIn: 'root'
})
export class TokenStorageService {
  constructor(private authService: AuthService) { }

  public signOut(): void {
    this.authService.logout().subscribe(
      data => {
        window.sessionStorage.clear();
      },
      err => {
        // return err.error.message;
      }
    );
    window.sessionStorage.clear();
  }

  public saveToken(token: string, refToken: string): void {
    window.sessionStorage.removeItem(TOKEN_KEY);
    window.sessionStorage.setItem(TOKEN_KEY, token);

    window.sessionStorage.removeItem(REFRESH_KEY);
    window.sessionStorage.setItem(REFRESH_KEY, refToken);
  }

  public getToken() {
    return this.checkTokenExp()

}

  public getRefToken(): string | null {
    const token = window.sessionStorage.getItem(REFRESH_KEY);
    return token;
  }

  public saveUser(user: any): void {
    window.sessionStorage.removeItem(USER_KEY);
    window.sessionStorage.setItem(USER_KEY, JSON.stringify(user));
  }

  public getUser(): any {
    const user = window.sessionStorage.getItem(USER_KEY);
    if (user) {
      return JSON.parse(user);
    }

    return {};
  }
  public checkTokenExp(): any  {
      let token = window.sessionStorage.getItem(TOKEN_KEY);
      let time =  Date.now();
      if (token) {
        console.log(atob(token.toString().split(".")[1]));
        const exp = JSON.parse(atob(token.toString().split(".")[1])).exp
        if ((exp * 1000) < (time)){
          console.log(exp * 1000);
          console.log(time);
          window.sessionStorage.removeItem(TOKEN_KEY);
          this.authService.tokenRefresh().subscribe(
            data => {
              this.saveToken(data.access_token, data.refresh_token);
              return(data.access_token)
            },
            err => {
              this.signOut();
            }
          );
        }
        
      }
      return(token)
  }
}
