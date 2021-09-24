import os
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import math
from datetime import date, timedelta

FB_ACCOUNT_FILE= os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
MSF_NFL_ID = os.getenv("MSF_NFL_ID")
MSF_NFL_SECRET= os.getenv("MSF_NFL_SECRET")
PICKS = ['pick_1', 'pick_2', 'pick_3']
DAY_0_OF_SEASON = date(2021, 9, 6)

class Test:
    def __init__(self):
        print(getWeekOfSeason())

class UpdateYesterdayRecords:

    def __init__(self):

        cred = credentials.Certificate(FB_ACCOUNT_FILE)
        firebase_admin.initialize_app(cred)
        db = firestore.client()

        dateYesterday = date.today() - timedelta(days = 1)

        # firebase crap
        users = db.collection(u'users')
        weekNumber = getWeekOfSeason()

        for user in users.get():

            week = users.document(user.id).collection('seasons').document('202122').collection('weeks').document(str(weekNumber)).get()
            weekRef = users.document(user.id).collection('seasons').document('202122').collection('weeks').document(str(weekNumber))

            for pick in PICKS:

                if(week.get(pick) != None):
                    thisPick = week.get(pick)

                    if thisPick.get('date') == str(dateYesterday):

                        pickDate = thisPick.get('date').replace("-", "")
                        team = thisPick.get('team')

                        response = requests.get(
                            f'https://api.mysportsfeeds.com/v1.2/pull/nfl/2021-regular/scoreboard.json?fordate={pickDate}&status=final&team={team}',
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
                        
                        if total > 0:
                            result = "W"
                        else:
                            result = "L"

                        weekRef.update({f"{pick}.result":f"{result}"})

def getWeekOfSeason():

    weekday = date.today().weekday()

    #Friday or Monday
    if(weekday == 4 or weekday == 0):
        return math.ceil(((date.today() - DAY_0_OF_SEASON).days)/7)

    return math.ceil(((date.today() - DAY_0_OF_SEASON).days)/7) - 1

UpdateYesterdayRecords()