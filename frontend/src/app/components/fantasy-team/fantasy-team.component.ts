import { Component, Input } from '@angular/core';
import { FantasyTeam } from '../../client/models/fantasy-team';

@Component({
  selector: 'fantasy-team',
  imports: [],
  templateUrl: './fantasy-team.component.html',
  styleUrl: './fantasy-team.component.css'
})
export class FantasyTeamComponent {
  @Input() team : FantasyTeam | undefined;
}
