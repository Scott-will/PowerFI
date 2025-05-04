import { Component, EventEmitter, Output } from '@angular/core';
import { TransactionType } from './transaction-types';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'transaction-type-selector',
  imports: [ FormsModule, CommonModule],
  templateUrl: './transaction-type-selector.component.html',
  styleUrl: './transaction-type-selector.component.css'
})
export class TransactionTypeSelectorComponent {
  @Output() transactionTypeChange = new EventEmitter<TransactionType>();
  transactionTypes = Object.values(TransactionType)
  transactionType: TransactionType = TransactionType.All

  onTransactionTypeChange() {
    console.log("emitting: ", this.transactionType)
    this.transactionTypeChange.emit(this.transactionType); 
  }
}
