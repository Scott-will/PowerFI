import logging

from sqlalchemy.ext.asyncio import AsyncSession

from PowerFIServer.server.TransactionCommon.TransactionTreeNode import TransactionTreeNode
from PowerFIServer.server.TransactionCommon.TransactionTypes import GetValidTransactionTypes
from PowerFIServer.server.db.Dao.transactions_dao import get_transactions, get_trades, get_waivers, get_transactions_for_player, \
    get_transactions_for_team, get_related_transactions, get_transaction_stats, get_player_transaction_stats
from PowerFIServer.server.db.models.transactions.transaction import Transaction

logger = logging.getLogger(__name__)

class TransactionsService:
    #paginated api to get players
    async def getTransactions(self, take : int, skip : int, player : str, team : str, type : str, db : AsyncSession) -> [Transaction]:
        if type:
            if type not in GetValidTransactionTypes():
                #throw error
                return []
        try:
            return await get_transactions(take, skip, player, team, type, db)
        except Exception as e:
            logger.error("Failed to get transactions", e)
            return []

    async def getTrades(self, take : int, skip : int, db : AsyncSession) -> [Transaction]:
        try:
            return await get_trades(take, skip, db)
        except Exception as e:
            logger.error("Failed to get trades", e)
            return []

    async def get_waivers(self, take: int, skip: int, db: AsyncSession) -> [Transaction]:
        try:
            return await get_waivers(take, skip, db)
        except Exception as e:
            logger.error("Failed to get waiver wire transactions", e)
            return []

    async def get_transactions_for_players(self, player_id : str, db : AsyncSession)-> [Transaction]:
        try:
            return await get_transactions_for_player(player_id, db)
        except Exception as e:
            logger.error("Failed to get transactions for player", player_id, e)
            return []

    async def get_transactions_for_teams(self, team_key : str, db : AsyncSession)-> [Transaction]:
        try:
            return await get_transactions_for_team(team_key, db)
        except Exception as e:
            logger.error("Failed to get transactions for team", team_key, e)
            return []

    async def get_transaction_stats(self, transaction_id : str, db : AsyncSession):
        try:
            await get_transaction_stats(transaction_id, db)
        except Exception as e:
            logger.error("Failed to get transactions stats for transaction: ", transaction_id, e)
            return []

    async def get_player_transaction_stats(self, player_id : str, db : AsyncSession):
        try:
            await get_player_transaction_stats(player_id, db)
        except Exception as e:
            logger.error("Failed to get transactions stats for player: ", player_id, e)
            return []

    async def get_related_transactions(self, transaction_id : str, db : AsyncSession) -> [TransactionTreeNode]:
        try:
            return await self.build_transaction_tree(transaction_id, db)
        except Exception as e:
            print(e)
            return []

    async def build_transaction_tree(self, transaction_id : str, db : AsyncSession) -> [TransactionTreeNode]:
        nodes = await self.get_nodes(transaction_id, {}, db)
        nodes.sort(key = lambda node: node.transaction.timestamp)
        start_node = self.link_nodes(nodes[0], nodes)
        return start_node

    async def get_nodes(self, transaction_id : str, seen_players :{}, db : AsyncSession) -> [TransactionTreeNode]:
        transactions = await get_related_transactions(transaction_id, db)
        nodes = [TransactionTreeNode(tx) for tx in transactions]
        unseen_players = self.populate_seen_players(seen_players, nodes[0].transaction)
        if len(unseen_players) != 0:
            nodes += await self.get_nodes(nodes[0].transaction.transaction_id, seen_players, db)
        return nodes

    def populate_seen_players(self, seen_players : {}, transaction : Transaction) -> [str]:
        players = list(set(transaction.added_players.split(",") + transaction.removed_players.split(",")))
        unseen_players = []
        for p in players:
            if not p:
                continue
            if seen_players.get(p) is None:
                seen_players[p] = p
                unseen_players.append(p)
        return unseen_players

    def link_nodes(self, start_node : TransactionTreeNode, nodes : [TransactionTreeNode]) -> TransactionTreeNode:
        players = list(set(start_node.transaction.added_players.split(",") + start_node.transaction.removed_players.split(",")))
        added_players = {}
        for p in players:
            if not p:
                continue
            for node in nodes:
                if ((p in node.transaction.added_players or p in node.transaction.removed_players)
                        and node.transaction.timestamp > start_node.transaction.timestamp
                and added_players.get(p) is None):
                    added_players[p] = p
                    start_node.children.append(self.link_nodes(node, nodes))
        return start_node







