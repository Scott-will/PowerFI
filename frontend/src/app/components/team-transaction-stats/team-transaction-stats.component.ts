import { Component } from '@angular/core';
import { FantasyTeamService } from '../../client/services/fantasy-team.service';
import { FantasyTeamCache } from '../../cache/fantasy-team-cache';
import { TeamTransactionStats } from '../../client/models/fantasy-team-transaction-stats';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'team-transaction-stats',
  imports: [CommonModule],
  templateUrl: './team-transaction-stats.component.html',
  styleUrl: './team-transaction-stats.component.css'
})
export class TeamTransactionStatsComponent {

  teams : TeamTransactionStats[] = [];
  sortColumn: string = 'total';
  sortDirection = true;

  constructor(private readonly fantasyTeamService : FantasyTeamService, private readonly fantasyTeamCache : FantasyTeamCache){}

  ngOnInit() {
    this.fetchTeamData();
  }

  fetchTeamData(){
    this.fantasyTeamService.getAllFantasyTeamStats({order_by:this.sortColumn, sort_asc : String(this.sortDirection)})
    .subscribe((response) => {
      this.teams = response
    })
    
  }

  getTeamName(team_key : string): string {
    return this.fantasyTeamCache.getTeamByKey(team_key)?.name?? ""
  }

  sortBy(column: string) {
    if (this.sortColumn === column) {
      this.sortDirection = !this.sortDirection;
    } else {
      this.sortColumn = column;
      this.sortDirection = true;
    }
    this.fetchTeamData()
  }
}
