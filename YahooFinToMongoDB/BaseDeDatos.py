from pymongo import *
import Herramientas as tool
from tqdm import *
from datetime import datetime
from yahoo_fin.stock_info import *


class BaseDeDatos:
    MTickets = ""
    MData = ""

    def __init__(self, client, db, collectionTickets, collectionData):
        self.setMongoDataBase(client, db, collectionTickets, collectionData)


    def setMongoDataBase(self, client, db, collectionTickets, collectionData):
        MClient = MongoClient(client)
        MDb = MClient[db]
        self.MTickets = MDb[collectionTickets]
        self.MData = MDb[collectionData]


    def updateTicketsCedears(self):
        cedears = []
        decicion = input("¿Quiere obtener los cedears de dow jones? dow jones tiene " + str(len(tickers_dow())) + " acciones en total: ")
        if(decicion == "y"):
            print("obteniendo cedears de dow jones")
            cedears += self.getCedearsFrom(tickers_dow())
        decicion = input("¿Quiere obtener los cedears de nasdaq? nasdaq tiene " + str(len(tickers_nasdaq())) + " acciones en total: ")
        if(decicion == "y"):
            print("obteniendo cedears de nasdaq")
            cedears += self.getCedearsFrom(tickers_nasdaq())
        decicion = input("¿Quiere obtener los cedears de sp500? sp500 tiene " + str(len(tickers_sp500())) + " acciones en total: ")
        if(decicion == "y"):
            print("obteniendo cedears de sp500")
            cedears += self.getCedearsFrom(tickers_sp500())

        for ticket in self.MTickets.find():
            for ticketActual in range(len(cedears)):
                if (ticket["TicketName"] == cedears[ticketActual]):
                    cedears.pop(ticketActual)
                    break
            if len(cedears) == 0:
                break

        for ticket in cedears:
            mydict = { "TicketName": ticket}
            self.MTickets.insert_one(mydict)

    def getCedearsFrom(self, tickets):
        ticketsAvaliables = []
        for ticket in tqdm(range(len(tickets))):
            ticketActual = tickets[ticket]
            try:
                data = get_data(ticketActual + ".ba", start_date="24/08/2020")
                ticketsAvaliables.append(ticketActual + ".ba")
            except:
                continue
        return ticketsAvaliables

    def subirCedearsDelDia(self, myOtherData):
        cedears = []
        for ticket in self.MTickets.find():
            cedears.append(ticket['TicketName'])
        updateInfo = {
            "fecha": datetime.now().strftime("%m/%d/%Y"),
            "cedears": [],
        }
        for cedear in tqdm(range(len(cedears))):
            info = tool.getInfoFewDaysAgo(1, datetime.now(), cedears[cedear])
            if type(info) != type(""):
                infoToUpdate = {
                    "ticket": cedears[cedear],
                    "open": info["open"][0],
                    "close": info["close"][0],
                    "high": info["high"][0],
                    "low": info["low"][0]
                }
                updateInfo["cedears"].append(infoToUpdate.copy())
        nro = 0
        for a in myOtherData.find({"fecha": datetime.now().strftime("%m/%d/%Y")}):
            nro += 1
        if nro > 0:
            myOtherData.update_one({"fecha": datetime.now().strftime("%m/%d/%Y")},
                                   {"$set": {"cedears": updateInfo["cedears"]}})
        else:
            myOtherData.insert_one(updateInfo)