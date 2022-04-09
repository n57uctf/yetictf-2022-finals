import { Injectable } from '@angular/core';
import { HttpRequest, HttpHandler, HttpEvent, HttpInterceptor, HttpResponse } from '@angular/common/http';
import { Observable, of, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

import { AuthService } from '../_services/auth.service';
import { Response } from '../_models/Response'

@Injectable()
export class ErrorInterceptor implements HttpInterceptor {
    constructor(private auth: AuthService) { }

    intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
        return next.handle(request).pipe(catchError(err => {
            
            let faked: Response = {
                success: false
            }

            if (err.status === 401) {
                // auto logout if 401 response returned from api
                this.auth.logout();
                location.reload();
            }

            const error = err.error.message || err.statusText;

            return of(
                new HttpResponse({
                    body:  faked,
                    url: "faked"
                })
            )
            //return throwError(error);
        }))
    }
}