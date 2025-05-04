export interface PlayerTransactionStats {
    id : number;
    player_key : string;
    total : number;
    trades : number;
    add: number;
    drop : number;
}

export interface PlayerTransactionStatsResponse{
    total : number;
    items : PlayerTransactionStats[];
}