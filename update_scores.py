import os
import requests

class UpdateScores:

    def __init__(self):
        ip = requests.get("https://icanhazip.com")
        print(ip.text)


UpdateScores()