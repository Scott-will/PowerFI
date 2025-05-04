export interface Player {
    id : number;
    player_id : string;
    player_key : string;
    position : string;
    first_name: string;
    last_name : string;
    team : string | null;
    picture : number;
    picture_url : string;
}

export interface PlayerResponse{
    total : number;
    items : Player[];
}