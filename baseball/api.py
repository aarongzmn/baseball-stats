import requests
from urllib.parse import urlencode, quote_plus


class Baseball:
    def __init__(self):
        self._host = "http://lookup-service-prod.mlb.com"


class PlayerData(Baseball):
    """Endpoints for getting general player data.
    This data typically includes important dates for the player (birth, pro debut),
    some basic attributes like throwing/batting arm, height,
    weight as well as country of birth and college/schools attended.
    https://appac.github.io/mlb-data-api-docs/#player-data
    """
    def search_for_players(self, search_name, pro=True, active=True) -> list:
        """https://appac.github.io/mlb-data-api-docs/#player-data-player-search
        search_name (str): First and/or Last name of the player you are searchign for.
        pro (bool): True if the player is in MLB, False if minor league player.
        active (bool): True if player is currently active. Use False for retired players.
        """
        params = {}
        if len(search_name.split(" ")) > 1:
            params["name_part"] = f"'{search_name}'"
        else:
            params["name_part"] = f"'{search_name}%'"
        if pro == True:
            params["sport_code"] = "'mlb'"
        else:
            params["sport_code"] = "'milb'"
            print("Need to verify if sport_code='milb' is correct parameter for minor leagues")
        if active == True:
            params["active_sw"] = "'Y'"
        else:
            params["active_sw"] = "'N'"

        encoded_params = urlencode(params, quote_via=quote_plus)
        endpoint = f"/json/named.search_player_all.bam?{encoded_params}"
        r = requests.get(self._host + endpoint)
        search_results = r.json()["search_player_all"]["queryResults"]["row"]
        result_type = type(search_results)
        if result_type == list:
            return search_results
        else:
            return [search_results]

    def get_player_details(self, player_id, pro=True) -> dict:
        """https://appac.github.io/mlb-data-api-docs/#player-data-player-info
        player_id (str): Player ID can be found using the 'search_player_all' method.
        pro (bool): True if the player is in MLB, False if minor league player.
        """
        params = {}
        params["player_id"] = f"'{player_id}'"
        if pro == True:
            params["sport_code"] = "'mlb'"
        else:
            params["sport_code"] = "'milb'"
            print("Need to verify if sport_code='milb' is correct parameter for minor leagues")

        encoded_params = urlencode(params, quote_via=quote_plus)
        endpoint = f"/json/named.search_player_all.bam?{encoded_params}"

        encoded_params = urlencode(params, quote_via=quote_plus)
        endpoint = f"/json/named.player_info.bam?{encoded_params}"
        r = requests.get(self._host + endpoint)
        return r.json()["player_info"]["queryResults"]["row"]


class StatsData(Baseball):
    """Endpoints for getting player stats. This data typically encompasses
    pitching/batting stats per season, league, game type and also projected stats.
    https://appac.github.io/mlb-data-api-docs/#stats-data
    """
    def season_hitting_stats(
        self,
        player_id: str,
        season: str,
        game_type: str = "R",
        pro: bool = True,
        ) -> dict:
        """Retrieve a players hitting stats for a given season.
        https://appac.github.io/mlb-data-api-docs/#stats-data-season-hitting-stats-get
        """
        params = {}
        params["player_id"] = player_id
        params["game_type"] = f"'{game_type}'"
        params["season"] = season
        if pro is True:
            params["league_list_id"] = "'mlb'"
        else:
            params["league_list_id"] = "'milb'"
            print("Need to verify if sport_code='milb' is correct parameter for minor leagues")

        encoded_params = urlencode(params, quote_via=quote_plus)
        endpoint = f"/json/named.sport_hitting_tm.bam?{encoded_params}"
        r = requests.get(self._host + endpoint)
        return r.json()["sport_hitting_tm"]["queryResults"].get("row")

    def season_pitching_stats(
        self,
        player_id: str,
        season: str,
        game_type: str = "R",
        pro: bool = True,
        ) -> dict:
        """Retrieve a players pitching stats for a given season.
        https://appac.github.io/mlb-data-api-docs/#stats-data-season-pitching-stats-get
        """
        params = {}
        params["player_id"] = player_id
        params["game_type"] = f"'{game_type}'"
        params["season"] = season
        if pro is True:
            params["league_list_id"] = "'mlb'"
        else:
            params["league_list_id"] = "'milb'"
            print("Need to verify if sport_code='milb' is correct parameter for minor leagues")

        encoded_params = urlencode(params, quote_via=quote_plus)
        endpoint = f"/json/named.sport_hitting_tm.bam?{encoded_params}"
        r = requests.get(self._host + endpoint)
        return r.json()["sport_hitting_tm"]["queryResults"].get("row")


class TeamData(Baseball):
    """Endpoints for getting team data. This data typically encompasses stadium information,
    contact details, and other team specific information.
    https://appac.github.io/mlb-data-api-docs/#team-data
    """
    def get_teams_by_season(
        self,
        season: str,
        allstar: bool = False
        ) -> dict:
        """Retrieve a list of major league teams that were active during a given season.
        https://appac.github.io/mlb-data-api-docs/#team-data-list-teams-get
        """
        params = {}
        params["season"] = f"'{season}'"
        if allstar:
            params["all_star_sw"] = "'Y'"
        else:
            params["all_star_sw"] = "'N'"
        encoded_params = urlencode(params, quote_via=quote_plus)
        endpoint = f"/json/named.team_all_season.bam?sport_code='mlb'&{encoded_params}"
        r = requests.get(self._host + endpoint)
        return r.json()["team_all_season"]["queryResults"]["row"]

    def get_40_man_roster(
        self,
        team_id: str,
        ) -> dict:
        """Retrieve a team's 40 man roster.
        https://appac.github.io/mlb-data-api-docs/#team-data-40-man-roster-get
        """
        endpoint = f"/json/named.roster_40.bam?team_id={team_id}"
        r = requests.get(self._host + endpoint)
        return r.json()["roster_40"]["queryResults"]["row"]
