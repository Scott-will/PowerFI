import { Component, Input, Output, EventEmitter } from '@angular/core';
import { TransactionService } from '../../client/services/transactions.service';
import { PlayerCache } from '../../cache/player-cache';
import { Player } from '../../client/models/player';
import { CommonModule } from '@angular/common';
import { Transaction, TreeNode } from '../../client/models/transaction';
import { response } from 'express';
import { FantasyTeamCache } from '../../cache/fantasy-team-cache';

@Component({
  selector: 'player-transaction-modal',
  imports: [CommonModule],
  templateUrl: './player-transaction-modal.component.html',
  styleUrl: './player-transaction-modal.component.css'
})
export class PlayerTransactionModalComponent {
  
  @Input() selectedPlayerId!: string;
  @Output() close = new EventEmitter<void>();
  selectedPlayer : Player|null = null;
  transactions : Transaction[] = [];
  
  constructor(
    private readonly transactionService: TransactionService,
    private readonly playerCache : PlayerCache,
    private readonly teamCache : FantasyTeamCache
  ) {
    this.transactionService = transactionService;
    this.playerCache = playerCache;
    this.teamCache = teamCache
  }

  ngOnInit(){
    this.selectedPlayer = this.playerCache.getPlayerById(this.selectedPlayerId) ?? null;
    this.transactionService.getPlayerTransactions(this.selectedPlayerId).subscribe((response) => {
      this.transactions = response
    })
    this.transactions.sort((a,b) => parseInt(a.timestamp) - parseInt(b.timestamp))
  }

  handlePlayerClick(playerId : string){
    this.selectedPlayer = this.playerCache.getPlayerById(playerId) ?? null
    this.transactionService.getPlayerTransactions(playerId)
  }

  closeModal(): void {
    this.selectedPlayer = null;
    this.close.emit()
  }

  getTeamImageUrl(team_key : string){
    let team = this.teamCache.getTeamByKey(team_key)
    return team?.picture_url
  }
}
