import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';


const API_URL = 'http://stevenik.nl:5000/user/';

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};

@Injectable({
  providedIn: 'root'
})
export class UserService {
  constructor(private http: HttpClient) { }

  getUserProfile(): Observable<any> {
    return this.http.get(API_URL + 'profile', { responseType: 'json' });
  }

  getProfilePicture(): Observable<any> {

    return this.http.get(API_URL + 'profile/picture', { responseType: 'blob' });
  }

  getAdminPage(): Observable<any> {
    return this.http.get(API_URL + 'admin', { responseType: 'text' });
  }

  updateUserProfile(email: string, first_name: string, last_name: string): Observable<any> {
    return this.http.post(API_URL + 'profile/update', {
      email,
      first_name,
      last_name
    }, httpOptions);
  }
}
