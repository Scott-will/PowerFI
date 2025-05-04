import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { ConfigService } from './config.services';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, RouterLink, RouterLinkActive, FormsModule, CommonModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'PowerFI';

  constructor(private readonly configService: ConfigService) {}
  
  ngOnInit(): void {
    // Load the config
    this.configService.loadConfig().subscribe(config => {
      this.configService.setApiUrl(config.apiUrl);
      console.log('API URL:', this.configService.getApiUrl());  // You can now use the API URL dynamically
    });
  }
}
