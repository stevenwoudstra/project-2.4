import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { ActivatedRouteSnapshot } from '@angular/router';

const AUTH_API = 'http://stevenik.nl:5000/user/';
// const AUTH_API = 'http://localhost:5000/user/';

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  constructor(private http: HttpClient) { }
  public isUserLoggedIn: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);

  login(username: string, password: string): Observable<any> {
    return this.http.post(AUTH_API + 'login', {
      username,
      password
    }, httpOptions);
  }

  afterLogin(): Observable<any> {
    return this.http.get(AUTH_API + 'info', {
    });
  }

  register(username: string, email: string, password: string): Observable<any> {
    return this.http.post(AUTH_API + 'register', {
      username,
      email,
      password
    }, httpOptions);
  }

  tokenRefresh(): Observable<any> {
    return this.http.post(AUTH_API + 'refresh', {
    });
  }

  logout(): Observable<any>  {
    return this.http.delete(AUTH_API + 'logout', {
    });
  }

  canUserAccess(route: ActivatedRouteSnapshot) {
    let logReg = ['login', 'register'];
    
    if(logReg.includes(route.url[0].toString())) return !this.isUserLoggedIn.value;
    return this.isUserLoggedIn.value;
  }
}
