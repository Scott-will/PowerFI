export interface TeamTransactionStats {
    id : number;
    team_key : string;
    total : number;
    trades : number;
    add: number;
    drop : number;
}

export interface TeamTransactionStatsResponse{
    total : number;
    items : TeamTransactionStats[];
}