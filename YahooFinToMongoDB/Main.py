from pymongo import *
from datetime import datetime, timedelta
import requests

from BaseDeDatos import BaseDeDatos

import json

import Indicadores as Indicator
import Herramientas as tool



jsonASubir = {
    "tipo_activo":"",
    "activo":"",
    "ticket":"",
    "fecha":"",
    "indicadores":[
        {
            "indicador":"STOCH",
            "curvas":{
                "slowk":[],
                "slowd":[]
            },
            "lineas_punteadas":[
                {
                    "nombre":"80",
                    "posicion_y":80
                },
                {
                    "nombre":"20",
                    "posicion_y":20
                }
            ],
            "etiquetas":[
                {
                    "nombre":"",
                    "posiciones":[]
                }
            ]
        },
        {
            "indicador":"DMI",
            "curvas":{
                "adx":[],
                "di_plus":[],
                "di_minus":[]
            }
        }
    ]
}

MyBase = BaseDeDatos("mongodb://localhost:27017/", "Market", "ticketsCedears", "cedearPureData")
MyBase.subirCedearsDelDia()

TICKET = "BPAT.BA"
DAYS = 30

data = tool.getInfoFewDaysAgo(DAYS, datetime.now(), TICKET)
stochData = Indicator.getStochasticIndicator(data)
ADXData = Indicator.getADXIndicator(data)
bBand = Indicator.getBollingerBands(data)

#showStoch(stochData, TICKET)
Indicator.showBBGraphic(bBand, data, TICKET)
Indicator.showADXGraphic(ADXData, TICKET)
Indicator.showStochGraphic(stochData, TICKET)

# subirCedearsDelDia(myOtherData)
# updateTicketsCedears("mongodb://localhost:27017/")

# get de heatMap (just 2 cedears for now)



"""
#save in database

for mapAndResult in range(len(xTrains)):
    mydict = {
        "heatmap": binary.Binary(pickle.dumps(xTrains[mapAndResult], protocol=2)),
        "result": int(yTrains[mapAndResult])
    }
    x = myData.insert_one(mydict)
"""


"""
------------------------------------------------
subirCedearsDelDia(myOtherData)

description:
update the cedear's data from today into the mongodb in the table "myOtherData"
------------------------------------------------
runIATest()

Description:
run a IA's Test
------------------------------------------------
getBollingerBands(ticket)

Description:
Give you the bollinger bands in a dict
 
The dict returned:
bollingerBand{
    prom:[],
    standarDesviation:[]
}
------------------------------------------------
getInfoFewDaysAgo(days,actualDate,ticket)

Description:
return the data from few days ago
------------------------------------------------
updateTicketsCedears(mongoClientUsed)

Description: 
Update the name of cedears's tickets in the database
------------------------------------------------
getCedearsFrom(tickets)

Description:
check in an array if it have valids cedears and give you the truly tickets
------------------------------------------------
getTokenBullMarket(dni,password)

Description:
with the dni and the password of an account in BullMarket give you a valid token 
"""