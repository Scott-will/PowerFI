import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Transaction } from '../../../client/models/transaction';
import { FantasyTeam } from '../../../client/models/fantasy-team';
import { PlayerCache } from '../../../cache/player-cache';
import { FantasyTeamCache } from '../../../cache/fantasy-team-cache';
@Component({
  selector: 'transaction-item',
  imports: [],
  templateUrl: './transaction-item.component.html',
  styleUrl: './transaction-item.component.css'
})
export class TransactionItemComponent {
  @Input() transaction : Transaction | undefined;
  @Input() fantasyTeams : FantasyTeam[] = [];
  showLists = false
  @Output() itemClicked = new EventEmitter<Transaction>();
  

  constructor(private readonly playerCache : PlayerCache){   }

  getFantasyTeamTradee() : FantasyTeam{
    return this.fantasyTeams[0]
  }

  getFantasyTeamTrader() : FantasyTeam{
    return this.fantasyTeams[1]
  }

  onMouseEnter(){
    this.showLists = true
  }

  onMouseLeave(){
    this.showLists = false
  }

  getPlayerName(id : string){
    return this.playerCache.getPlayerNameById(id)
  }

  onClick(){
    console.log("Clicked!!")
    this.itemClicked.emit(this.transaction)
  }

}
