import logging
from datetime import datetime, timedelta

import requests
from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession
from yfpy import YahooFantasySportsQuery, League, Transaction

from PowerFIServer.server.db.Dao.fantasy_team_dao import save_fantasy_teams
from PowerFIServer.server.db.Dao.players_dao import save_players
from PowerFIServer.server.db.Dao.transactions_dao import save_transactions
from PowerFIServer.server.db.models.teams.fantasy_team import FantasyTeam
from PowerFIServer.server.db.models.players.player import Player
from PowerFIServer.server.db.models.players.player_image import PlayerImage
from PowerFIServer.server.db.models.teams.fantasy_team_image import FantasyTeamImage
from PowerFIServer.server.db.models.transactions.player_stats_transactions import PlayerStatsByTransaction
from PowerFIServer.server.db.models.transactions.transaction import Transaction, TransactionPlayers

logger = logging.getLogger(__name__)

class YahooEngine:
    def __init__(self):
        self.query : YahooFantasySportsQuery = None
        self.league_id : str = ""

    def initQuery(self, league_id):
        if self.query is None or self.league_id != league_id:
            self.query = YahooFantasySportsQuery(league_id=league_id, game_code="nba")
            self.league_id = league_id

    async def get_league_data(self, league_id, db : AsyncSession):
        self.initQuery(league_id)
        response = self.query.get_league_info()
        try:
            await self.load_players(db)
        except Exception as e:
            logger.error("Failed to save players:", e)
        try:
            await self.load_fantasy_teams(response, db)
        except Exception as e:
            logger.error("Failed to save teams:", e)
        try:
            await self.load_transactions(response, db)
        except Exception as e:
            logger.error("Failed to save transactions:", e)
        ##Commented out since yahoo rate limits
        #try:
         #   await self.get_player_points_during_transaction_period(db)
        #except Exception as e:
         #   logger.error("Failed to save transaction data:", e)

    async def load_players(self, db : AsyncSession):
        players = []
        playersResponse = self.query.get_league_players()
        try:
            for player_data in playersResponse:
                try:
                    player = Player(player_data.player_id, player_data.player_key, player_data.first_name, player_data.last_name,
                        player_data.display_position, player_data.editorial_team_full_name)
                    players.append(player)
                except Exception as e:
                    logger.error("Failed to create player:", e)
            await save_players(players, db)
        except Exception as e:
            logger.error("Failed to save players:", e)

        players = await db.execute(select(Player))
        players = players.scalars().all()
        try:
            results = [(p.id, p.player_id) for p in players]
            for player in results:
                player_metadata = next((p for p in playersResponse if p.player_id == player[1]), None)
                if player_metadata != None:
                    player_image = await self.save_player_image( player_metadata.headshot.url, player[0])
                    db.add(player_image)
                    await db.flush()  # Flush to generate the ID
                    stmt = update(Player).where(Player.id == player[0]).values(picture_url=f"http://localhost:80/api/players/get_player_image/{player_image.id}")
                    await db.execute(stmt)
                    await db.commit()
        except Exception as e:
            logger.error("Failed to load players", e)

    async def load_fantasy_teams(self, response : League,  db : AsyncSession):
        teams = []
        for team_data in response.teams:
            team = FantasyTeam(team_data.team_id, team_data.name.decode("utf-8"), team_data.manager.nickname, team_data.team_key)
            teams.append(team)
        await save_fantasy_teams(teams, db)
        teams = await db.execute(select(FantasyTeam))
        teams = teams.scalars().all()
        try:
            results = [(t.id, t.team_id) for t in teams]
            for team in results:
                team_metadata = next((t for t in response.teams if t.team_id == team[1]), None)
                if team_metadata != None:
                    fantasy_team_image = await self.save_fantasy_team_image(team_metadata.team_logos[0].url, team[0])
                    db.add(fantasy_team_image)
                    await db.flush()  # Flush to generate the ID
                    stmt = update(FantasyTeam).where(FantasyTeam.id == team[0]).values(
                        picture_url=f"http://localhost:80/api/teams/get_team_image/{fantasy_team_image.id}")
                    await db.execute(stmt)
                    await db.commit()
        except Exception as e:
            print(e)

    async def load_transactions(self, response : League,  db : AsyncSession):
        transactions = []
        for transaction_data in response.transactions:
            try:
                transaction_players = self.extractPlayersFromTransaction(transaction_data)
                transaction = Transaction(
                    transaction_data.transaction_id,
                    transaction_data.timestamp,
                    transaction_data.type,
                    transaction_data.status,
                    transaction_players)
                transactions.append(transaction)
            except Exception as e:
                print("failed for transaction", transaction_data.transaction_id)
                print(e)
        await save_transactions(transactions, db)

    async def save_player_image(self, url : str, player_id : int) -> PlayerImage | None:
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            image_data = r.content
            content_type = r.headers.get("Content-Type", "application/octet-stream")
            player_image = PlayerImage(player_id, image_data, content_type)
            return player_image
        else:
            return None

    async def save_fantasy_team_image(self, url : str, fantasy_team_id : int) -> FantasyTeamImage | None:
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            image_data = r.content
            content_type = r.headers.get("Content-Type", "application/octet-stream")
            team_image = FantasyTeamImage(fantasy_team_id, image_data, content_type)
            return team_image
        else:
            return None

    def extractPlayersFromTransaction(self, transaction) -> TransactionPlayers:
        transaction_players = TransactionPlayers()
        transaction_players.addedPlayers = []
        transaction_players.removedPlayers = []
        try:
            if transaction.type == 'trade':
                transaction_players.addedTeam = transaction.tradee_team_key
                transaction_players.removedTeam = transaction.trader_team_key
                for player in transaction.players:
                    if player.transaction_data.destination_team_key == transaction_players.addedTeam:
                        transaction_players.addedPlayers.append(player.player_id)
                    elif player.transaction_data.destination_team_key == transaction_players.removedTeam:
                        transaction_players.removedPlayers.append(player.player_id)
            elif transaction.type == 'add':
                for player in transaction.players:
                    transaction_players.addedPlayers.append(player.player_id)
                    transaction_players.removedTeam = "Waiver"
                    transaction_players.addedTeam = player.transaction_data.destination_team_key
            elif transaction.type == 'drop':
                for player in transaction.players:
                    transaction_players.removedPlayers.append(player.player_id)
                    transaction_players.addedTeam = "Waiver"
                    transaction_players.removedTeam = player.transaction_data.source_team_key
            elif transaction.type == 'add/drop':
                for player in transaction.players:
                    if player.transaction_data.destination_team_key:
                        transaction_players.addedPlayers.append(player.player_id)
                        transaction_players.removedTeam = "Waiver"
                        transaction_players.addedTeam = player.transaction_data.destination_team_key
                    else:
                        transaction_players.removedPlayers.append(player.player_id)
        except Exception as e:
            print(e)
        return transaction_players

    ##Causes yahoo to block api calls
    async def get_player_points_during_transaction_period(self, db : AsyncSession):
        transactions = self.query.get_league_transactions()
        transactions.sort(key=lambda x: x.timestamp)
        season_end = datetime.now()
        players = await db.execute(select(Player))
        players = players.scalars().all()
        for p in players:
            player_transactions = []
            target_player_name = p.first_name + " " + p.last_name
            for transaction in transactions:
                for player in transaction.players:
                    if player.name.full == target_player_name:
                        player_transactions.append({
                            'timestamp': transaction.timestamp,
                            'player_key': p.player_key,
                            'transaction_key': transaction.transaction_key,
                            'fantasy_points': 0.0
                        })

            for i in range(0, len(player_transactions)-2):
                player_transactions[i]['fantasy_points'] = await self.get_player_stats_for_transaction(p.player_key,
                                       datetime.utcfromtimestamp(player_transactions[i]["timestamp"]).strftime('%Y-%m-%d'),
                                       datetime.utcfromtimestamp(player_transactions[i+1]["timestamp"]).strftime('%Y-%m-%d'))
            if len(player_transactions) > 0:
                player_transactions[-1]['fantasy_points'] = await self.get_player_stats_for_transaction(p.player_key,
                                   datetime.utcfromtimestamp(player_transactions[-1]["timestamp"]).strftime('%Y-%m-%d'),
                                                                                              season_end.strftime('%Y-%m-%d'))
            for pt in player_transactions:
                db.add(PlayerStatsByTransaction(pt['player_key'], pt['transaction_key'], pt['fantasy_points']))

    ##Causes yahoo to block api calls
    async def get_player_stats_for_transaction(self, player_key : str, start : str, end : str) -> float:
        total = 0.0
        current_date = start

        while current_date <= end:
            stats = await self.query.get_player_stats_by_date(player_key, current_date)

            try:
                total += stats.player_points_value
            except (KeyError, TypeError, ValueError):
                continue


            date_obj = datetime.strptime(current_date, '%Y-%m-%d')
            new_date = date_obj + timedelta(days=1)
            current_date = new_date.strftime('%Y-%m-%d')

        return total

yahoo_engine = YahooEngine()