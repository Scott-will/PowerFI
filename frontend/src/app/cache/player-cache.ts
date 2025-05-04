import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { Player } from '../client/models/player';
import { PlayerService } from '../client/services/players.service';

@Injectable({
  providedIn: 'root'
})

export class PlayerCache {
    private readonly playerIdMap = new Map<number, Player>();
    private readonly playerKeyMap = new Map<string, number>();

    constructor(private readonly playerService : PlayerService){
        this.loadCache();
    }

    loadCache(){
        const players = this.playerService.getAllPlayers({skip : '0', take : '1000000', order_by:"player_id", sort_asc : "true"})
        players.forEach(player => {
            player.items.forEach(x =>{
                this.playerIdMap.set(parseInt(x.player_id), x);
                this.playerKeyMap.set(x.player_key, parseInt(x.player_id))
            })
          });
          console.log("Successfully loaded cache:", this.playerIdMap.size)
    }

    getPlayerById(id : string): Player | undefined{
        const player = this.playerIdMap.get(parseInt(id))
        if(!player){
            console.log("Did not find player with id: ", id)
            return undefined
        }
        return player
    }

    getPlayerNameById(playerId : string){
        const player = this.getPlayerById(playerId)
        if(player == undefined){
            return ""
        }
        return `${player.first_name} ${player.last_name}`;        
    }

    getPlayerByKey(key : string): Player | undefined{
        const id = this.playerKeyMap.get(key)
        if(!id){
            console.log("Did not find player with id: ", key)
            return undefined
        }
        return this.getPlayerById(id.toString())
    }

    getPlayerNameByKey(key : string){
        const player = this.getPlayerByKey(key)
        if(player == undefined){
            return ""
        }
        return `${player.first_name} ${player.last_name}`;        
    }
}