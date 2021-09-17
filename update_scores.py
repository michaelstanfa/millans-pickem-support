import os
import requests
import json
from datetime import date
import math

MSF_NFL_ID = os.getenv("MSF_NFL_ID")
MSF_NFL_SECRET= os.getenv("MSF_NFL_SECRET")

DAY_0_OF_SEASON = date(2021, 9, 8)

class UpdateScores:

    def __init__(self):

        today = date.today().strftime("%Y%m%d")

        today = 20210912
        # response = requests.get("https://api.mysportsfeeds.com/v1.2/pull/nfl/2021-regular/full_game_schedule.json", auth=(MSF_NFL_ID, MSF_NFL_SECRET))
        response = requests.get(
            f'https://api.mysportsfeeds.com/v1.2/pull/nfl/2021-regular/scoreboard.json?fordate={today}&status=final',
            auth=(MSF_NFL_ID, MSF_NFL_SECRET))
        r = response.json()

        games = r['scoreboard']['gameScore']
        
        for game in games:
            print(game["game"]["ID"])
            print(game["awayScore"])
            print(game["homeScore"])

        # today = date.today()
        # this_week = getWeekOfSeason(today)

        # week_games = [x for x in games if x['week'] == str(this_week)]
        # week_games = [x for x in games if x['week'] == str(1)]
        # print(week_games)

def getWeekOfSeason(today):
    #this actually represents the number of weeks
    return math.ceil(((today - DAY_0_OF_SEASON).days)/7)

UpdateScores()
