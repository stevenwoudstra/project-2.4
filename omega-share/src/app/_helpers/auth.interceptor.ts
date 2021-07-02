import { HTTP_INTERCEPTORS, HttpEvent } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { HttpInterceptor, HttpHandler, HttpRequest } from '@angular/common/http';

import { TokenStorageService } from '../_services/token-storage.service';
import { Observable } from 'rxjs';

const TOKEN_HEADER_KEY = 'Authorization';
const TYPE = 'Bearer '

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  constructor(private token: TokenStorageService) { }

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    let authReq = req;
    const token = this.token.getToken();
    const refToken = this.token.getRefToken();
    if (token != null) {
      const kaas: string = TYPE + token;
      authReq = req.clone({ headers: req.headers.set(TOKEN_HEADER_KEY, kaas).set('Cache-Control', 'no-cache, no-store, must-revalidate')
      .set('Pragma', 'no-cache')
      });
    } else if((refToken != null) && (req.url.endsWith("/user/refresh"))){
      console.log(req)
      const kaas: string = TYPE + refToken;
      authReq = req.clone({ headers: req.headers.set(TOKEN_HEADER_KEY, kaas) });
    }
    return next.handle(authReq);
  }
}

export const authInterceptorProviders = [
  { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true }
];

