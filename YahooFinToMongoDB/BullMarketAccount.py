import requests
import json

class Account:
    mail = ""
    dni = ""
    psw = ""

    def __init__(self, mail, dni, psw):
        self.mail = mail
        self.dni = dni
        self.psw = psw

    def getTokenBullMarket(self):
        url = "https://bullmarketbrokers.com/Home/Login"

        payload = {
            'idNumber': self.dni,
            'password': self.psw
        }

        headers = {
            'Cookie': 'ASP.NET_SessionId=et443mc4ngbnfe5suw541bhf; 7572a1cd-608b-45e4-b6a7-fdb52f674e8c=UserId=UJhud7cd59jbcDYUz0dLvw==; lastUserIdLogged=lastUserIdLogged=113203; notificationCookie=notifications={"type1":[],"type2":[]}'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        response = response.text.encode('utf-8')
        response = json.loads(response)

        if response['succeed']:
            return response['token']
        return 'Failure'