import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ConfigService {
  private apiUrl: string = '';

  constructor(private readonly http: HttpClient) {}

  // Load the config file on app initialization
  loadConfig(): Observable<any> {
    return this.http.get('assets/config.json');
  }

  getApiUrl(): string {
    return this.apiUrl;
  }

  setApiUrl(url: string): void {
    this.apiUrl = url;
  }
}
