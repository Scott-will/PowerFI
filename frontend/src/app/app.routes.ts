import { Routes } from '@angular/router';
import { PlayerListComponent } from './components/players/playerList.component';
import { FantasyTeamListComponent } from './components/fantasy-team-list/fantasy-team-list.component';
import { TransactionPageComponent } from './components/Transactions/transaction-page/transaction-page.component';
import { PlayerTransactionStatsComponent } from './components/player-transaction-stats/player-transaction-stats.component';
import { TeamTransactionStatsComponent } from './components/team-transaction-stats/team-transaction-stats.component';
export const routes: Routes = [
    {path: 'playerList', component: PlayerListComponent},
    {path: 'transaction-page', component: TransactionPageComponent},    
    {path: 'team-transaction-stats', component: TeamTransactionStatsComponent},
    {path: 'player-transaction-stats', component: PlayerTransactionStatsComponent},
    { path: '', redirectTo: '/playerList', pathMatch: 'full' }, // Default route
];
