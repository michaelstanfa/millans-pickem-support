import os
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import math
from datetime import date

FB_ACCOUNT_FILE= os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
MSF_NFL_ID = os.getenv("MSF_NFL_ID")
MSF_NFL_SECRET= os.getenv("MSF_NFL_SECRET")
PICKS = ['pick_1', 'pick_2', 'pick_3']
DAY_0_OF_SEASON = date(2021, 9, 6)

class UpdateWeekRecords:

    def __init__(self):

        cred = credentials.Certificate(FB_ACCOUNT_FILE)
        firebase_admin.initialize_app(cred)
        db = firestore.client()

        # firebase crap
        users = db.collection(u'users')
        weekNumber = getWeekOfSeason()

        for user in users.get():

            week = users.document(user.id).collection('seasons').document('202122').collection('weeks').document(weekNumber).get()
            weekRef = users.document(user.id).collection('seasons').document('202122').collection('weeks').document(weekNumber)

            for pick in PICKS:
                print(pick)
                if(week.get(pick) != None):
                    thisPick = week.get(pick)
                    date = thisPick.get('date').replace("-", "")
                    print(date)
                    team = thisPick.get('team')
                    print(team)
                    response = requests.get(
                        f'https://api.mysportsfeeds.com/v1.2/pull/nfl/2021-regular/scoreboard.json?fordate={date}&status=final&team={team}',
                        auth=(MSF_NFL_ID, MSF_NFL_SECRET))
                    r = response.json()

                    home = True if r['scoreboard']['gameScore'][0]['game']['homeTeam']['Abbreviation'] == team else False
                    homeScore = float(r['scoreboard']['gameScore'][0]['homeScore'])
                    line = float(thisPick.get('line'))
                    awayScore = float(r['scoreboard']['gameScore'][0]['awayScore'])
                    if(home):
                        total = homeScore + line - awayScore
                    else:
                        total = awayScore + line - homeScore
                    
                    print(total)
                    if total > 0:
                        result = "W"
                    else:
                        result = "L"

                    weekRef.update({f"{pick}.result":f"{result}"})

def getWeekOfSeason():

    return math.ceil(((date.today() - DAY_0_OF_SEASON).days)/7) - 1

UpdateWeekRecords()