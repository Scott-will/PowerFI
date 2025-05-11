import pytest
from unittest.mock import patch, AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession

from PowerFIServer.server.db.models.teams.fantasy_team import FantasyTeam
from PowerFIServer.server.db.models.teams.fantasy_team_image import FantasyTeamImage
from PowerFIServer.server.db.models.teams.fantasy_team_transaction_stats import FantasyTeamTransactionStats
from PowerFIServer.server.services.fantasyTeamsService import FantasyTeamsService

mock_db = AsyncMock(spec=AsyncSession)

@pytest.mark.asyncio
async def test_get_fantasy_teams_success():
    mock_teams = [
        FantasyTeam(team_id="t1", name="Team 1", manager_name="Manager 1", team_key="Key 1"),
        FantasyTeam(team_id="t2", name="Team 2", manager_name="Manager 2", team_key="Key 2"),
    ]
    with patch('PowerFIServer.server.services.fantasyTeamsService.get_fantasy_teams', AsyncMock(return_value = mock_teams)):
        service = FantasyTeamsService()
        result = await service.getFantasyTeams(take=10, skip=0, db=mock_db)
        assert len(result) == 2
        assert result[0].team_id == "t1"
        assert result[1].team_id == "t2"
        assert result[0].name == "Team 1"
        assert result[1].name == "Team 2"

@pytest.mark.asyncio
async def test_get_fantasy_teams_fail():
    with patch('PowerFIServer.server.db.Dao.fantasy_team_dao.get_fantasy_teams', AsyncMock(side_effect=Exception("DB Error"))):
        service = FantasyTeamsService()
        result = await service.getFantasyTeams(take=10, skip=0, db=mock_db)
        assert result == []

@pytest.mark.asyncio
async def test_get_fantasy_team_image_success():
    mock_image = FantasyTeamImage(1, "abcd", "image")
    with patch.object(FantasyTeamsService, 'get_fantasy_team_image', AsyncMock(return_value=mock_image)):
        service = FantasyTeamsService()
        result = await service.get_fantasy_team_image(1, mock_db)
        assert result.fantasy_team_id == mock_image.fantasy_team_id

@pytest.mark.asyncio
async def test_get_fantasy_team_image_fail():
    with patch('PowerFIServer.server.db.Dao.fantasy_team_dao.get_fantasy_teams',
               AsyncMock(side_effect=Exception("DB Error"))):
        service = FantasyTeamsService()
        result = await service.getFantasyTeams(take=10, skip=0, db=mock_db)
        assert result == []


@pytest.mark.asyncio
async def test_get_team_transaction_stats_success():
    mock_teams = [
        FantasyTeamTransactionStats(team_key="abc"),
        FantasyTeamTransactionStats(team_key="abc")
    ]
    mock_teams[0].add = 5
    mock_teams[1].add = 10
    with patch.object(FantasyTeamsService, 'get_team_transaction_stats', AsyncMock(return_value=mock_teams)):
        service = FantasyTeamsService()
        result = await service.get_team_transaction_stats("abc", mock_db)
        assert result[0].team_key == mock_teams[0].team_key
        assert result[1].team_key == mock_teams[1].team_key
        assert result[0].add == mock_teams[0].add
        assert result[1].add == mock_teams[1].add

@pytest.mark.asyncio
async def test_get_team_transaction_stats_fail():
    with patch('PowerFIServer.server.db.Dao.fantasy_team_dao.get_team_transaction_stats',
               AsyncMock(side_effect=Exception("DB Error"))):
        service = FantasyTeamsService()
        result = await service.get_team_transaction_stats("abc", mock_db)
        assert result is None

@pytest.mark.asyncio
async def test_get_all_team_transaction_stats_success():
    mock_teams = [
        FantasyTeamTransactionStats(team_key="abc"),
        FantasyTeamTransactionStats(team_key="abc")
    ]
    mock_teams[0].add = 5
    mock_teams[1].add = 10
    with patch.object(FantasyTeamsService, 'get_all_team_transaction_stats',
               AsyncMock(return_value=mock_teams)):
        service = FantasyTeamsService()
        result = await service.get_all_team_transaction_stats("total",True, mock_db)
        assert result[0].team_key == mock_teams[0].team_key
        assert result[1].team_key == mock_teams[1].team_key
        assert result[0].add == mock_teams[0].add
        assert result[1].add == mock_teams[1].add

@pytest.mark.asyncio
async def test_get_all_team_transaction_stats_fail():
    with patch('PowerFIServer.server.db.Dao.fantasy_team_dao.get_all_team_transaction_stats',
               AsyncMock(side_effect=Exception("DB Error"))):
        service = FantasyTeamsService()
        result = await service.get_all_team_transaction_stats("total", True, mock_db)
        assert result is None