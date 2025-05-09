import { Component, OnInit } from '@angular/core';
import { FantasyTeam } from '../../client/models/fantasy-team';
import { FantasyTeamService } from '../../client/services/fantasy-team.service';
import { FantasyTeamComponent } from "../fantasy-team/fantasy-team.component";

@Component({
  selector: 'fantasy-team-list',
  imports: [FantasyTeamComponent],
  templateUrl: './fantasy-team-list.component.html',
  styleUrl: './fantasy-team-list.component.css'
})
export class FantasyTeamListComponent implements OnInit{
  teams : FantasyTeam[] = [];
  
  constructor(private readonly fantasyTeamService : FantasyTeamService){} 

  ngOnInit(): void {
    this.fetchTransactionData()
  }

  fetchTransactionData(){
    this.fantasyTeamService.getAllFantasyTeams()
    .subscribe((response) => {
      this.teams = response
    })
  }
}
