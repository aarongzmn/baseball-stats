import requests
import datetime

from urllib.parse import urlencode, quote_plus


class PlayerData:
    """Endpoints for getting general player data.
    This data typically includes important dates for the player (birth, pro debut),
    some basic attributes like throwing/batting arm, height,
    weight as well as country of birth and college/schools attended.
    https://appac.github.io/mlb-data-api-docs/#player-data
    """
    def __init__(self, host):
        self._host = host

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


class StatsData:
    """Endpoints for getting player stats. This data typically encompasses
    pitching/batting stats per season, league, game type and also projected stats.
    https://appac.github.io/mlb-data-api-docs/#stats-data
    """
    def __init__(self, host):
        self._host = host

    def season_hitting_stats(
        self,
        player_id: str,
        game_type: str = "R",
        season: str = str(datetime.datetime.now().year - 1),
        pro: bool = True,
        ) -> list:
        """https://appac.github.io/mlb-data-api-docs/#stats-data-season-hitting-stats-get
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
        return r.json()["sport_hitting_tm"]["queryResults"]
