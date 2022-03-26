from . import api


class Baseball:
    def __init__(self):
        self._host = "http://lookup-service-prod.mlb.com"
        self.player_data = api.PlayerData(self._host)
        self.stats_data = api.StatsData(self._host)
