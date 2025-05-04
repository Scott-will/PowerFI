import { Component, OnInit } from '@angular/core';
import { PlayerService } from '../../client/services/players.service';
import { Player } from '../../client/models/player';
import {MatPaginator, PageEvent} from '@angular/material/paginator';

@Component({
  selector: 'playerList',
  templateUrl: './playerList.component.html',
  styleUrls: ['./playerList.component.css'],
  imports: [
    MatPaginator
 ],
})
export class PlayerListComponent implements OnInit {
  players : Player[] = [];
  totalItems = 0;
  pageSize = 10;
  pageIndex = 0;

  constructor(private readonly playerService: PlayerService) {}

  ngOnInit() {
    this.fetchPlayerData(); // Fetch the players when the component initializes
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
}
