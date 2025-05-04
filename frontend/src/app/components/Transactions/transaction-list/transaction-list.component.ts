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

@Component({
  selector: 'transaction-list',
  templateUrl: './transaction-list.component.html',
  styleUrl: './transaction-list.component.css',
  imports: [
    MatPaginator,
    TransactionItemComponent,
    FormsModule,
    TransactionTypeSelectorComponent
],
})

export class TransactionListComponent implements OnInit{
  playerName = "";
  transactionTypes = Object.values(TransactionType);
  transactionType = TransactionType.All;
  
  transactions : Transaction[] = [];
  totalItems = 0;
  pageSize = 10;
  pageIndex = 0;
  @Output() selectedTransaction = new EventEmitter<Transaction>();

  constructor(
    private readonly transactionService : TransactionService,
    private readonly fantasyTeamCache : FantasyTeamCache){}

  ngOnInit(): void {
    this.fetchTransactionData()
  }

  onTransactionTypeChanged(newTransactionType: TransactionType) {
    this.transactionType = newTransactionType;
    console.log("Update transaction type to: ", this.transactionType, newTransactionType)
  }
  
  fetchTransactionData(){
    console.log(this.transactionType)
    this.transactionService.getAllTransactions({skip: (this.pageIndex*this.pageSize).toString(), take : this.pageSize.toString(), type : this.transactionType})
    .subscribe((response) => {
      this.transactions = response.items
      this.totalItems = response.total
    })
  }

  getFantasyTeams(transaction: Transaction): FantasyTeam[] {
    const addedTeam = this.fantasyTeamCache.getTeamByKey(transaction.team_key_added);
    const removedTeam = this.fantasyTeamCache.getTeamByKey(transaction.team_key_removed);
    return [addedTeam, removedTeam].filter(team => team !== undefined && team !== null);
  }
  

  onPageChange(event: PageEvent): void {
    this.pageIndex = event.pageIndex;
    this.pageSize = event.pageSize;
    this.fetchTransactionData();
  }

  onSearchSubmit(): void {
    this.pageIndex = 0; // Reset to the first page
    this.fetchTransactionData();
  }

  onItemClicked(transaction: Transaction) {
    console.log("List CLICKED!!")
    this.selectedTransaction.emit(transaction);
  }
}
