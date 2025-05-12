import { Injectable } from '@angular/core';
import { FantasyTeam } from '../models/fantasy-team';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ConfigService } from '../../config.services';
import { TeamTransactionStats } from '../models/fantasy-team-transaction-stats';
import { environment } from '../../environment/environment';

@Injectable({
    providedIn: 'root'
  })
export class FantasyTeamService {
   
    constructor(private readonly http: HttpClient, private readonly configService: ConfigService){}

    private readonly baseUrl = environment.apiUrl;
    private readonly getTeamsUrl = "/api/teams/get_fantasy_teams?take=1000&skip=0"
    private readonly getTeamStatsUrl = "/api/teams/get_all_team_transaction_stats"

    getAllFantasyTeams(): Observable<[FantasyTeam]> {
        return this.http.get<[FantasyTeam]>(this.baseUrl + this.getTeamsUrl);      
    }

    getAllFantasyTeamStats(queryParams : {[key : string]:string}): Observable<[TeamTransactionStats]> {
        let params = new HttpParams();
        for (const key in queryParams) {
            if (queryParams.hasOwnProperty(key)) {
            params = params.set(key, queryParams[key]);
            }
        }
        return this.http.get<[TeamTransactionStats]>(this.baseUrl + this.getTeamStatsUrl, {params});      
    }
}