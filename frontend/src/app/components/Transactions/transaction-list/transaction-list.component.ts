import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { TransactionService } from '../../../client/services/transactions.service';
import { Transaction } from '../../../client/models/transaction';
import {MatPaginator, PageEvent} from '@angular/material/paginator';
import { TransactionItemComponent } from '../transaction-item/transaction-item.component';
import { FantasyTeam } from '../../../client/models/fantasy-team';
import { TransactionType } from '../transaction-type-selector/transaction-types';
import { FormsModule } from '@angular/forms';
import { TransactionTypeSelectorComponent } from "../transaction-type-selector/transaction-type-selector.component";
import { FantasyTeamCache } from '../../../cache/fantasy-team-cache';
import { PaginationHelper } from '../../../helpers/pagination-helper';
import { CommonModule } from '@angular/common';
import { PlayerCache } from '../../../cache/player-cache';

@Component({
  selector: 'transaction-list',
  templateUrl: './transaction-list.component.html',
  styleUrl: './transaction-list.component.css',
  imports: [
    FormsModule,
    TransactionTypeSelectorComponent,
    CommonModule
],
})

export class TransactionListComponent implements OnInit{
  playerName = "";
  teamName = "";
  transactionTypes = Object.values(TransactionType);
  transactionType = TransactionType.All;
  
  transactions : Transaction[] = [];
  paginationHelper! : PaginationHelper;
  
  @Output() selectedTransaction = new EventEmitter<Transaction>();

  constructor(
    private readonly transactionService : TransactionService,
    private readonly fantasyTeamCache : FantasyTeamCache,
    private readonly playerCache : PlayerCache){
      this.playerCache = playerCache
      this.paginationHelper = new PaginationHelper(this.fetchTransactionData.bind(this))
    }

  ngOnInit(): void {
    this.fetchTransactionData()
  }

  onTransactionTypeChanged(newTransactionType: TransactionType) {
    this.transactionType = newTransactionType;
  }
  
  fetchTransactionData(){
    this.transactionService.getAllTransactions({skip: ((this.paginationHelper.pageIndex-1)*this.paginationHelper.pageSize).toString(), take : this.paginationHelper.pageSize.toString(), type : this.transactionType, player : this.playerName, team : this.teamName})
    .subscribe((response) => {
      this.transactions = response.items
      this.paginationHelper.totalItems = response.total
      console.log("total is: ", response.total)
    })
  }

  getFantasyTeam(team_key: string): string {
      const addedTeam = this.fantasyTeamCache.getTeamByKey(team_key);
      return addedTeam?.name ?? "";
  }  

  getPlayerNames(players: string): string {
    const playerKeys = players.split(',');
    return playerKeys
      .map(p => this.playerCache.getPlayerNameById(p))
      .join(', ');
  }
  

  onSearchSubmit(): void {
    this.paginationHelper.pageIndex = 1;
    this.fetchTransactionData();
  }

  onItemClicked(transaction: Transaction) {
    this.selectedTransaction.emit(transaction);
  }
}
