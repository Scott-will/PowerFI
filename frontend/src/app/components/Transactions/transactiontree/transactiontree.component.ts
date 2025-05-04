import { Component, Input } from '@angular/core';
import { Transaction, TreeNode } from '../../../client/models/transaction';
import { CommonModule } from '@angular/common';
import { TransactionService } from '../../../client/services/transactions.service';
import { TransactionItemComponent } from "../transaction-item/transaction-item.component";
import { FantasyTeamCache } from '../../../cache/fantasy-team-cache';
import { FantasyTeam } from '../../../client/models/fantasy-team';

@Component({
  selector: 'transactiontree',
    imports: [CommonModule, TransactionItemComponent],
  templateUrl: './transactiontree.component.html',
  styleUrl: './transactiontree.component.css'
})
export class TransactiontreeComponent {
  @Input() node!: TreeNode;

  constructor(private readonly fantasyTeamCache : FantasyTeamCache){
    this.fantasyTeamCache = fantasyTeamCache;
  }
  getFantasyTeams(transaction: Transaction): FantasyTeam[] {
      const addedTeam = this.fantasyTeamCache.getTeamByKey(transaction.team_key_added);
      const removedTeam = this.fantasyTeamCache.getTeamByKey(transaction.team_key_removed);
      return [addedTeam, removedTeam].filter(team => team !== undefined && team !== null);
    }
}
