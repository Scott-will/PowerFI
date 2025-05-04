import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { AppComponent } from './app/app.component';

bootstrapApplication(AppComponent, appConfig)
  .catch((err) => console.error(err));

  /*
  todo:
* refactor player list and player

*link teams to trades

*sub menu for trades, pickups 

*build waiver model*/