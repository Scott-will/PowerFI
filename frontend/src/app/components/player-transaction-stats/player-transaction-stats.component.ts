import { Component } from '@angular/core';
import { PlayerService } from '../../client/services/players.service';
import { PlayerTransactionStats } from '../../client/models/player-transaction-stats';
import { PageEvent } from '@angular/material/paginator';
import { CommonModule } from '@angular/common';
import { PlayerCache } from '../../cache/player-cache';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'player-transaction-stats',
  imports: [CommonModule, FormsModule],
  templateUrl: './player-transaction-stats.component.html',
  styleUrl: './player-transaction-stats.component.css'
})
export class PlayerTransactionStatsComponent {

  players : PlayerTransactionStats[] = [];
  totalItems = 0;
  pageSize = 10;
  pageSizeOptions = [5, 10, 20, 50];
  pageIndex = 1;
  sortColumn: string = 'total';
  sortDirection = true;

  constructor(private readonly playerService : PlayerService, private readonly playerCache : PlayerCache){}

  ngOnInit() {
    this.fetchPlayerData();
  }

  fetchPlayerData(){
    console.log(this.pageIndex, this.pageSize)
    this.playerService.getAllPlayerStats({skip: ((this.pageIndex-1)*this.pageSize).toString(), take : this.pageSize.toString(), order_by:this.sortColumn, sort_asc : String(this.sortDirection)})
    .subscribe((response) => {
      this.players = response.items
      this.totalItems = response.total
    })
    
  }
  
    get totalPages() {
      return Math.ceil(this.totalItems / this.pageSize);
    }

    goToPage(page: number) {
      if (page >= 1 && page <= this.totalPages) {
        this.pageIndex = page;
        this.fetchPlayerData();
      }
    }
    nextPage() {
      this.goToPage(this.pageIndex + 1);
      this.fetchPlayerData();
    }
  
    prevPage() {
      this.goToPage(this.pageIndex - 1);
      this.fetchPlayerData();
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
