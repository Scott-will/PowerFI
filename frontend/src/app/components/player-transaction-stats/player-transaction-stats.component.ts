import { Component } from '@angular/core';
import { PlayerService } from '../../client/services/players.service';
import { PlayerTransactionStats } from '../../client/models/player-transaction-stats';
import { PageEvent } from '@angular/material/paginator';
import { CommonModule } from '@angular/common';
import { PlayerCache } from '../../cache/player-cache';
import { FormsModule } from '@angular/forms';
import { PaginationHelper } from '../../helpers/pagination-helper';

@Component({
  selector: 'player-transaction-stats',
  imports: [CommonModule, FormsModule],
  templateUrl: './player-transaction-stats.component.html',
  styleUrl: './player-transaction-stats.component.css'
})
export class PlayerTransactionStatsComponent {

  players : PlayerTransactionStats[] = [];
  paginationHelper! : PaginationHelper
  sortColumn: string = 'total';
  sortDirection = true;

  constructor(private readonly playerService : PlayerService, 
    private readonly playerCache : PlayerCache){
      this.paginationHelper = new PaginationHelper(this.fetchPlayerData.bind(this))
    }

  ngOnInit() {
    this.fetchPlayerData();
  }

  fetchPlayerData(){
    console.log(this.paginationHelper.pageIndex, this.paginationHelper.pageSize)
    this.playerService.getAllPlayerStats({skip: ((this.paginationHelper.pageIndex-1)*this.paginationHelper.pageSize).toString(), take : this.paginationHelper.pageSize.toString(), order_by:this.sortColumn, sort_asc : String(this.sortDirection)})
    .subscribe((response) => {
      this.players = response.items
      this.paginationHelper.totalItems = response.total
    })
    
  }
  

  getPlayerName(playerKey : string): string{
    return this.playerCache.getPlayerNameByKey(playerKey)
  }

  sortBy(column: string) {
    if (this.sortColumn === column) {
      this.sortDirection = !this.sortDirection;
    } else {
      this.sortColumn = column;
      this.sortDirection = true;
    }
    this.fetchPlayerData()
  }

}
