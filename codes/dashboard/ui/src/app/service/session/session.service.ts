import { api } from '../../shared/config';
import { Injectable } from '@angular/core';
import { HttpClientModule, HttpClient } from '@angular/common/http';
import { HttpHeaders } from '@angular/common/http';
import { catchError, map, tap } from 'rxjs/operators';

@Injectable()
export class SessionService {
  root = api.root;

  constructor(private http: HttpClient) {}
  
  getSessionSeq(req) {
    const httpOptions = {
      headers: new HttpHeaders({ 'Content-Type': 'application/json' }),
    };
    const url = this.root + 'session/session/' + req.sessId;
    return this.http.get(url).pipe(tap(data => {}));
  }

  getValueCounts(req) {
    const httpOptions = {
      headers: new HttpHeaders({ 'Content-Type': 'application/json' }),
    };
    const url = this.root + 'session/common?col='+req.col+'&max='+req.max;
    return this.http.get(url).pipe(tap(data => {}));
  }

}
