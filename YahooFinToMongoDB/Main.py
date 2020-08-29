from bson import binary
from yahoo_fin.stock_info import *
from tqdm import *
from pymongo import *
import json
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pickle
from keras.utils import np_utils
import tensorflow as tf

def getTokenBullMarket(dni,password):
    url = "https://bullmarketbrokers.com/Home/Login"

    payload = {'idNumber': str(dni),
    'password': password}

    headers = {
      'Cookie': 'ASP.NET_SessionId=et443mc4ngbnfe5suw541bhf; 7572a1cd-608b-45e4-b6a7-fdb52f674e8c=UserId=UJhud7cd59jbcDYUz0dLvw==; lastUserIdLogged=lastUserIdLogged=113203; notificationCookie=notifications={"type1":[],"type2":[]}'
    }

    response = requests.request("POST", url, headers=headers, data = payload)

    response = response.text.encode('utf-8')
    response = json.loads(response)

    if(response['succeed']):
        return response['token']
    return 'Failure'

def getCedearsFrom(tickets):
    ticketsAvaliables = []
    for ticket in tqdm(range(len(tickets))):
        ticketActual = tickets[ticket]
        try:
            data = get_data(ticketActual + ".ba",start_date="24/08/2020")
            ticketsAvaliables.append(ticketActual + ".ba")
        except:
            continue
    return ticketsAvaliables

def updateTicketsCedears(mongoClientUsed):
    cedears = []
    decicion = input("¿Quiere obtener los cedears de dow jones? dow jones tiene " + str(len(tickers_dow())) + " acciones en total: ")
    if(decicion == "y"):
        print("obteniendo cedears de dow jones")
        cedears += getCedearsFrom(tickers_dow())
    decicion = input("¿Quiere obtener los cedears de nasdaq? nasdaq tiene " + str(len(tickers_nasdaq())) + " acciones en total: ")
    if(decicion == "y"):
        print("obteniendo cedears de nasdaq")
        cedears += getCedearsFrom(tickers_nasdaq())
    decicion = input("¿Quiere obtener los cedears de sp500? sp500 tiene " + str(len(tickers_sp500())) + " acciones en total: ")
    if(decicion == "y"):
        print("obteniendo cedears de sp500")
        cedears += getCedearsFrom(tickers_sp500())

    myclient = MongoClient(mongoClientUsed)
    mydb = myclient["Market"]
    mycol = mydb["ticketsCedears"]

    for ticket in mycol.find():
        for ticketActual in range(len(cedears)):
            if (ticket["TicketName"] == cedears[ticketActual]):
                cedears.pop(ticketActual)
                break
        if len(cedears) == 0:
            break

    for ticket in cedears:
        mydict = { "TicketName": ticket}
        x = mycol.insert_one(mydict)

def getInfoFewDaysAgo(days,actualDate,ticket):
    date_N_days_ago = actualDate - timedelta(days=days)
    dateInStringStart = str(date_N_days_ago.month) + "/" + str(date_N_days_ago.day) + "/" + str(date_N_days_ago.year)
    dateInStringEnd = str(actualDate.month) + "/" + str(actualDate.day) + "/" + str(actualDate.year)
    print("getInfoFewDaysAgo: " + str(days))

    return get_data(ticket, start_date=dateInStringStart,end_date=dateInStringEnd)

def getBollingerBands(days,actualDate,ticket):
    data = getInfoFewDaysAgo(days, actualDate, ticket)
    standarsDesviations = []
    aux = data.loc[:, ['open', 'close', 'high', 'low']]
    totalDays = data['open'].to_numpy().__len__()
    dataPastTest = getInfoFewDaysAgo(days*2, actualDate, ticket)
    for day in range(totalDays):
        dataPast = dataPastTest.iloc[day:totalDays+day]
        promediosPast = dataPast.loc[:, ['open', 'close', 'high', 'low']]
        standarsDesviations.append(np.std(promediosPast.mean(1).to_numpy()))
    BollingerBand = {
        'prom': aux.mean(1).to_numpy(),
        "standarDesviation": standarsDesviations
    }
    return BollingerBand

def acotation(max,min,num):
    return int(((num - min) / (max - min)) * 99)


def createTrainsDataCedears(dateToStart):
    DAYS = 30

    date_time = datetime.fromisoformat(dateToStart)
    xTrains = []
    yTrains = []
    yTest = []
    xTest = []
    cedears = []
    for cedear in mycol.find():
        cedears.append(cedear['TicketName'])
    trainOrTest = True
    for NroCedear in tqdm(range(2)):
        cedearTicket = cedears[NroCedear]
        prom = (getInfoFewDaysAgo(1, date_time + timedelta(days=1), cedearTicket))
        prom = [prom["open"][0], prom["close"][0], prom["high"][0], prom["low"][0]]
        prom = np.mean(prom)
        print(DAYS)
        data = getInfoFewDaysAgo(DAYS, date_time, cedearTicket)
        Bands = getBollingerBands(DAYS, date_time, cedearTicket)
        xQuantity = len(Bands['prom'])
        heatMap = np.zeros((100, xQuantity))
        for xPos in range(xQuantity):
            yPos = acotation(np.max(data['high']), np.min(data['low']), Bands['prom'][xPos])
            yPosClose = acotation(np.max(data['high']), np.min(data['low']), data['close'][xPos])
            yPosOpen = acotation(np.max(data['high']), np.min(data['low']), data['open'][xPos])

            if (yPosOpen < yPosClose):
                heat = 100
                plus = 80 / (yPosClose - yPosOpen)
                for y in range(yPosOpen, yPosClose):
                    heatMap[y][xPos] = int(heat)
                    heat += plus
            elif (yPosClose < yPosOpen):
                heat = 180
                substrac = 80 / (yPosOpen - yPosClose)
                for y in range(yPosClose, yPosOpen):
                    heatMap[y][xPos] = int(heat)
                    heat -= substrac
            heatMap[yPos][xPos] = 255
        if trainOrTest:
            yTrains.append(acotation(np.max(data["high"]), np.min(data["low"]), prom))
            xTrains.append(heatMap.copy())
        else:
            yTest.append(acotation(np.max(data["high"]), np.min(data["low"]), prom))
            xTest.append(heatMap.copy())
        trainOrTest = not trainOrTest
    yTrains = np.array(yTrains)
    xTrains = np.array(xTrains)
    yTest = np.array(yTest)
    xTest = np.array(xTest)

    return xTrains, yTrains, xTest, yTest


myclient = MongoClient("mongodb://localhost:27017/")


mydb = myclient["Market"]
mycol = mydb["ticketsCedears"]
myData = mydb["cedearData"]

#get de heatMap (just 2 cedears for now)
xTrains, yTrains, xTest, yTest = createTrainsDataCedears("2020-08-26")

"""
#save in database

for mapAndResult in range(len(xTrains)):
    mydict = {
        "heatmap": binary.Binary(pickle.dumps(xTrains[mapAndResult], protocol=2)),
        "result": int(yTrains[mapAndResult])
    }
    x = myData.insert_one(mydict)
"""

#adapt the data

xTrains.reshape(xTrains.shape[0], xTrains.shape[1]*xTrains.shape[2])
xTest.reshape(xTest.shape[0], xTest.shape[1]*xTest.shape[2])

xTrains = xTrains/100
xTest = xTest/100

yTrains = np_utils.to_categorical(yTrains, 100)
yTest = np_utils.to_categorical(yTest, 100)

#create the model

class MyModel(tf.keras.Model):

  def __init__(self):
    super(MyModel, self).__init__()
    self.dense1 = tf.keras.layers.Dense(32, input_dim=2100, activation=tf.nn.relu)
    self.dense2 = tf.keras.layers.Dense(10, activation=tf.nn.softmax)
    self.dropout = tf.keras.layers.Dropout(0.5)

  def call(self, inputs):
      x = self.dense1(inputs)
      return self.dense2(x)

#use the model

model = MyModel()

model.compile(optimizer='sgd', loss='categorical_crossentropy', metrics=['accuracy'])

model.fit(x=xTrains, y=yTrains, batch_size=100, epochs=10, verbose=1, validation_data=(xTest, yTest))

model.evaluate(x=xTest, y=yTest, batch_size=100, verbose=1)


"""
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