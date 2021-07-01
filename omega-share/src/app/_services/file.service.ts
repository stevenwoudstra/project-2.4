import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';


const API_URL = 'http://localhost:5000/';

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'multipart/form-data' })
};

@Injectable({
  providedIn: 'root'
})
export class FileService {
  constructor(private http: HttpClient) { }

  postProfilePicture(file: any): Observable<any> {
    const data = new FormData();
    data.append('file', file)

    return this.http.post(API_URL + 'file/upload/profile', data)
  }
  
}
