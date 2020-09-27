from datetime import datetime, timedelta

from BaseDeDatos import BaseDeDatos

import Indicadores as Indicator
import Herramientas as tool

MyBase = BaseDeDatos("mongodb://localhost:27017/", "Market", "ticketsCedears", "cedearPureData")
MyBase.updateTicketsCedears()
MyBase.subirIndicesYDatosDelDia()

TICKET = "BPAT.BA"
DAYS = 30

data = tool.getInfoFewDaysAgo(DAYS, datetime.now(), TICKET, 10)
stochData = Indicator.getStochasticIndicator(data)
ADXData = Indicator.getADXIndicator(data)
bBand = Indicator.getBollingerBands(data)

print(stochData)
print("-----------------------------")
print(ADXData)
print("-----------------------------")
print(bBand)
print("-----------------------------")



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
getInfoFewDaysAgo(days,actualDate,ticket, tolerance)

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