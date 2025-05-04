import { Component } from '@angular/core';
import { Transaction, TreeNode } from '../../../client/models/transaction';
import { TransactionListComponent } from "../transaction-list/transaction-list.component";
import { TransactiontreeComponent } from "../transactiontree/transactiontree.component";
import { CommonModule } from '@angular/common';
import { TransactionService } from '../../../client/services/transactions.service';

@Component({
  selector: 'transaction-page',
  imports: [CommonModule, TransactionListComponent, TransactiontreeComponent],
  templateUrl: './transaction-page.component.html',
  styleUrl: './transaction-page.component.css'
})
export class TransactionPageComponent {
  showTree = false;
  selectedItem! : Transaction;
  node! : TreeNode;

  constructor(private readonly transactionService : TransactionService){
    this.transactionService = transactionService
  }
  
  onTransactionSelected(item: Transaction){
    console.log("IT WAS CLICKED")
    this.selectedItem = item;
    this.getTransactionTree()
    this.showTree = true
  }

  getTransactionTree(){
    console.log("getting transactions for: ", this.selectedItem.transaction_id)
    this.transactionService.getTransactionTree(this.selectedItem.transaction_id)
    .subscribe((response) => {
      console.log(response)
      this.node = response;
    })
  }
}
