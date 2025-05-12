import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Transaction, TransactionResponse, TreeNode } from '../models/transaction';
import { ConfigService } from '../../config.services';
import { environment } from '../../environment/environment';


@Injectable({
    providedIn: 'root'
  })
export class TransactionService {
   
    constructor(private readonly http: HttpClient, private readonly configService: ConfigService){}

    private readonly getTransactionUrl = "/api/transactions/get_transactions?"
    private readonly getTradesUrl = "/api/transactions/get_trades?"
    private readonly getTransactionTreeUrl = "/api/transactions/related_transactions"
    private readonly getPlayerTransactionsUrl = "/api/transactions/player_transactions?"
    private readonly baseUrl = environment.apiUrl;
    
    getAllTransactions(queryParams : {[key : string]:string}): Observable<TransactionResponse> {
        let params = new HttpParams();
        for (const key in queryParams) {
            if (queryParams.hasOwnProperty(key)) {
            params = params.set(key, queryParams[key]);
            }
        }

        return this.http.get<TransactionResponse>(this.baseUrl + this.getTransactionUrl, { params });      
    }

    getAllTrades(queryParams : {[key : string]:string}): Observable<TransactionResponse> {
        let params = new HttpParams();
        for (const key in queryParams) {
            if (queryParams.hasOwnProperty(key)) {
            params = params.set(key, queryParams[key]);
            }
        }

        return this.http.get<TransactionResponse>(this.baseUrl + this.getTradesUrl, { params });      
    }

    getTransactionTree(transactionId : string): Observable<TreeNode>{
        let params = new HttpParams();
        params = params.set("transaction_id", transactionId)
        return this.http.get<TreeNode>(this.baseUrl + this.getTransactionTreeUrl, {params})
    }

    getPlayerTransactions(playerId : string): Observable<Transaction[]>{
        let params = new HttpParams();
        params = params.set("player_id", playerId)
        return this.http.get<Transaction[]>(this.baseUrl + this.getPlayerTransactionsUrl, {params})
    }
}