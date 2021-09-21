import os
import requests
import json
from datetime import date
import math
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
# import firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

MSF_NFL_ID = os.getenv("MSF_NFL_ID")
MSF_NFL_SECRET= os.getenv("MSF_NFL_SECRET")
FB_ACCOUNT_FILE= os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
DAY_0_OF_SEASON = date(2021, 9, 6)

class UpdateScores:

    def __init__(self):

        cred = credentials.Certificate(FB_ACCOUNT_FILE)
        firebase_admin.initialize_app(cred)
        db = firestore.client()

        today = date.today().strftime("%Y%m%d")
        # getting games for today
        today = 20210916
        response = requests.get(
            f'https://api.mysportsfeeds.com/v1.2/pull/nfl/2021-regular/scoreboard.json?fordate={today}&status=final',
            auth=(MSF_NFL_ID, MSF_NFL_SECRET))
        r = response.json()
        games = r['scoreboard']['gameScore']
        
        week = str(getWeekOfSeason())

        # firebase crap
        lines = db.collection(u'lines')
        docRef = lines.document(u'202122').collection(u'week').document(week)

        for game in games:
            if(game['isCompleted']):
                docRef.update({
                    f'game.{game["game"]["ID"]}.away_team.score': game["awayScore"],
                    f'game.{game["game"]["ID"]}.home_team.score': game["homeScore"],
                    f'game.{game["game"]["ID"]}.final': True
                })

def getWeekOfSeason():
    #this actually represents the number of weeks
    ## for testing
    return math.ceil(((date(2021, 9, 20) - DAY_0_OF_SEASON).days)/7)

    ## for real
    # return math.ceil(((date.today() - DAY_0_OF_SEASON).days)/7)

UpdateScores()
