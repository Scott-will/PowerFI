export interface Transaction {
    id : number;
    transaction_id : string;
    type : string;
    timestamp: string;
    status : string;
    added_players : string;
    removed_players : string;
    team_key_added : string;
    team_key_removed : string
}

export interface TransactionResponse{
    total : number;
    items : Transaction[];
}

export interface TreeNode {
    transaction: Transaction;
    children: TreeNode[];
  }