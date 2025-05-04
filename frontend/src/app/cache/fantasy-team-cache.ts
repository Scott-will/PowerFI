import { Injectable } from "@angular/core";
import { FantasyTeam } from "../client/models/fantasy-team";
import { FantasyTeamService } from "../client/services/fantasy-team.service";

@Injectable({
    providedIn: 'root'
})

export class FantasyTeamCache{
    private readonly fantasyTeamIdMap = new Map<string, FantasyTeam>();

    constructor(private readonly fantasyTeamService : FantasyTeamService){
        this.loadCache();
    }

    loadCache(){
        const teams = this.fantasyTeamService.getAllFantasyTeams()
        teams.forEach(team => {
            team.forEach(x =>{
                this.fantasyTeamIdMap.set(x.team_key, x)
            })
        })
        console.log("Successfully loaded team cache:", this.fantasyTeamIdMap.size)
    }

    getTeamByKey(id : string): FantasyTeam | undefined{
        const team = this.fantasyTeamIdMap.get(id)
        if(!team){
            console.log("Did not team with id: ", id)
            return undefined;
        }
        return team;
    }


}