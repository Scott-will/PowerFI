import { Injectable } from '@angular/core';
import { PlayerResponse } from '../models/player';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ConfigService } from '../../config.services';
import { PlayerTransactionStatsResponse } from '../models/player-transaction-stats';

@Injectable({
    providedIn: 'root'
  })
export class PlayerService {
   
    constructor(private readonly http: HttpClient, private readonly configService: ConfigService){}

    private readonly getPlayerUrl = "/api/players/get_players?"
    private readonly getPlayerStatsUrl = "/api/players/get_player_transaction_stats?"

    getAllPlayers(queryParams : {[key : string]:string}): Observable<PlayerResponse> {
        let params = new HttpParams();
        for (const key in queryParams) {
            if (queryParams.hasOwnProperty(key)) {
            params = params.set(key, queryParams[key]);
            }
        }

        return this.http.get<PlayerResponse>(this.configService.getApiUrl() + this.getPlayerUrl, { params });      
    }

    getAllPlayerStats(queryParams : {[key : string]:string}): Observable<PlayerTransactionStatsResponse> {
        let params = new HttpParams();
        for (const key in queryParams) {
            if (queryParams.hasOwnProperty(key)) {
            params = params.set(key, queryParams[key]);
            }
        }

        return this.http.get<PlayerTransactionStatsResponse>(this.configService.getApiUrl() + this.getPlayerStatsUrl, { params }); 
    }
}