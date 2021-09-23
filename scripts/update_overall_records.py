import os
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

FB_ACCOUNT_FILE= os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
MSF_NFL_ID = os.getenv("MSF_NFL_ID")
MSF_NFL_SECRET= os.getenv("MSF_NFL_SECRET")
PICKS = ['pick_1', 'pick_2', 'pick_3']

class UpdateOverallRecords:

    def __init__(self):

        cred = credentials.Certificate(FB_ACCOUNT_FILE)
        firebase_admin.initialize_app(cred)
        db = firestore.client()

        # firebase crap
        users = db.collection(u'users')

        for user in users.get():

            wins = 0
            losses = 0
            
            weeks = users.document(user.id).collection('seasons').document('202122').collection('weeks').get()
            for week in weeks:
                for pick in PICKS:
                    try:
                        if week.get(f'{pick}.result') == "W":
                            wins += 1
                        else:
                            losses += 1
                    except:
                        print("Games haven't been played yet. Hold your horses.")

            scoreRef = users.document(user.id).collection('seasons').document('202122')
            scoreRef.update({
                'wins': wins,
                'losses': losses
            })

UpdateOverallRecords()
