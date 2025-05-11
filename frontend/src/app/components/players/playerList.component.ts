import { Component, OnInit } from '@angular/core';
import { PlayerService } from '../../client/services/players.service';
import { Player } from '../../client/models/player';
import {MatPaginator, PageEvent} from '@angular/material/paginator';
import { CommonModule } from '@angular/common';
import { TransactionService } from '../../client/services/transactions.service';
import { PlayerCache } from '../../cache/player-cache';
import { PlayerTransactionModalComponent } from "../player-transaction-modal/player-transaction-modal.component";

@Component({
  selector: 'playerList',
  templateUrl: './playerList.component.html',
  styleUrls: ['./playerList.component.css'],
  imports: [
    MatPaginator,
    CommonModule,
    PlayerTransactionModalComponent
],
})
export class PlayerListComponent implements OnInit {
  players : Player[] = [];
  totalItems = 0;
  pageSize = 10;
  pageIndex = 0;
  showModal = false;
  selectedPlayerId = ""

  constructor(private readonly playerService: PlayerService,
    private readonly transactionService: TransactionService,
    private readonly playerCache : PlayerCache
  ) {
    this.playerService = playerService;
    this.transactionService = transactionService;
    this.playerCache = playerCache;
  }

  ngOnInit() {
    this.fetchPlayerData();
  }

  fetchPlayerData(){
    console.log(this.pageIndex, this.pageSize)
    this.playerService.getAllPlayers({skip: (this.pageIndex*this.pageSize).toString(), take : this.pageSize.toString(), order_by:"first_name", sort_asc : "true"})
    .subscribe((response) => {
      this.players = response.items
      this.totalItems = response.total
    })
    
  }

  onPageChange(event: PageEvent): void {
    this.pageIndex = event.pageIndex;
    this.pageSize = event.pageSize;
    this.fetchPlayerData();
  }

  openModal(playerId : string){
    this.showModal = true;
    this.selectedPlayerId = playerId;
  }

  closeModal(){
    this.showModal = false;
    this.selectedPlayerId = ""
  }
}
