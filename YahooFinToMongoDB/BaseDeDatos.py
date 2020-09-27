from pymongo import *
import Herramientas as tool
import Indicadores as indicator
from tqdm import *
from datetime import datetime, timedelta
from yahoo_fin.stock_info import *
import json


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
            tickets = tickers_dow()
            baTickets = []
            for ticket in tickets:
                baTickets.append(ticket + ".ba")
            cedears += self.getCedearsFromYahoo(baTickets)
        decicion = input("¿Quiere obtener los cedears de nasdaq? nasdaq tiene " + str(len(tickers_nasdaq())) + " acciones en total: ")
        if(decicion == "y"):
            print("obteniendo cedears de nasdaq")
            tickets = tickers_nasdaq()
            baTickets = []
            for ticket in tickets:
                baTickets.append(ticket + ".ba")
            cedears += self.getCedearsFromYahoo(baTickets)
        decicion = input("¿Quiere obtener los cedears de sp500? sp500 tiene " + str(len(tickers_sp500())) + " acciones en total: ")
        if(decicion == "y"):
            print("obteniendo cedears de sp500")
            tickets = tickers_sp500()
            baTickets = []
            for ticket in tickets:
                baTickets.append(ticket + ".ba")
            cedears += self.getCedearsFromYahoo(baTickets)

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

    def getCedearsFromYahoo(self, tickets):
        ticketsAvaliables = []
        for ticket in tqdm(range(len(tickets))):
            ticketActual = tickets[ticket]
            try:
                data = get_data(ticketActual, start_date=datetime.now() - timedelta(days=3))
                ticketsAvaliables.append(ticketActual)
            except:
                continue
        return ticketsAvaliables

    def fromCursorGetJson(self,cursor):
        documentInJson = {}
        for document in cursor:
            documentInJson = document
        return documentInJson

    def subirIndicesYDatosDelDia(self):
        ticketNro = 0
        total = self.MTickets.find().count()
        for ticket in self.MTickets.find():
            ticketNro += 1
            if ticketNro == 21:
                a = 1
            print("ticket nro: " + str(ticketNro) + " de: " + str(total))
            data = tool.getInfoFewDaysAgo(20, datetime.now(), ticket["TicketName"], 10)
            if type(data) != type(""):
                bbans = indicator.getBollingerBandsToday(data)
                stoch = indicator.getStochasticToday(data)
                adx = indicator.getADXToday(data)
                dataToday = data.iloc[-1]
                cantidad = self.MData.find({"ticket": ticket["TicketName"]}).count()
                actionCursor = self.MData.find({"ticket": ticket["TicketName"]})
                for action in actionCursor:
                    if cantidad > 0:
                        subirFecha = action["fechas"]
                        if subirFecha[-1] != datetime.now().strftime("%m/%d/%Y"):
                            subirFecha.append(datetime.now().strftime("%m/%d/%Y"))

                            #Indicadores
                            indicadoresGuardados = action["indicadores"]

                            indicadoresGuardados[0]["curvas"]["slowk"].append(stoch["STOCHk_5"])
                            indicadoresGuardados[0]["curvas"]["slowd"].append(stoch["STOCHd_3"])

                            indicadoresGuardados[1]["curvas"]["adx"].append(adx["ADX_14"])
                            indicadoresGuardados[1]["curvas"]["di_plus"].append(stoch["DMP_14"])
                            indicadoresGuardados[1]["curvas"]["di_minus"].append(stoch["DMN_14"])

                            indicadoresGuardados[2]["curvas"]["BBUp"].append(bbans["BBU_5_2.0"])
                            indicadoresGuardados[2]["curvas"]["BBMed"].append(stoch["BBM_5_2.0"])
                            indicadoresGuardados[2]["curvas"]["BBLow"].append(stoch["BBL_5_2.0"])

                            #Datos
                            datosGuardados = action["datos"]
                            datosGuardados["open"].append(dataToday["open"])
                            datosGuardados["close"].append(dataToday["close"])
                            datosGuardados["high"].append(dataToday["high"])
                            datosGuardados["low"].append(dataToday["low"])
                        else:
                            subirFecha[-1] = datetime.now().strftime("%m/%d/%Y")

                            #Indicadores
                            indicadoresGuardados = action["indicadores"]
                            indicadoresGuardados[0]["curvas"]["slowk"][-1] = stoch["STOCHk_5"]
                            indicadoresGuardados[0]["curvas"]["slowk"][-1] = stoch["STOCHd_3"]

                            indicadoresGuardados[1]["curvas"]["adx"][-1] = adx["ADX_14"]
                            indicadoresGuardados[1]["curvas"]["di_plus"][-1] = adx["DMP_14"]
                            indicadoresGuardados[1]["curvas"]["di_minus"][-1] = adx["DMN_14"]

                            indicadoresGuardados[2]["curvas"]["BBUp"][-1] = bbans["BBU_5_2.0"]
                            indicadoresGuardados[2]["curvas"]["BBMed"][-1] = bbans["BBM_5_2.0"]
                            indicadoresGuardados[2]["curvas"]["BBLow"][-1] = bbans["BBL_5_2.0"]

                            #Datos
                            datosGuardados = action["datos"]

                            datosGuardados["open"][-1] = dataToday["open"]
                            datosGuardados["close"][-1] = dataToday["close"]
                            datosGuardados["high"][-1] = dataToday["high"]
                            datosGuardados["low"][-1] = dataToday["low"]

                        self.MData.update_one({"ticket": ticket["TicketName"]},
                                              {"$set": {"indicadores": indicadoresGuardados, "datos": datosGuardados}})
                    else:
                        jsonIndicadoresASubir = {
                            "tipo_activo": "cedear",
                            "activo": "",
                            "ticket": ticket["TicketName"],
                            "fechas": [datetime.now().strftime("%m/%d/%Y")],
                            "indicadores": [
                                {
                                    "indicador": "STOCH",
                                    "curvas": {
                                        "slowk": [stoch["STOCHk_5"]],
                                        "slowd": [stoch["STOCHd_3"]],
                                    },
                                    "lineas_punteadas": [
                                        {
                                            "nombre": "80",
                                            "posicion_y": 80
                                        },
                                        {
                                            "nombre": "20",
                                            "posicion_y": 20
                                        }
                                    ],
                                    "etiquetas": [
                                        {
                                            "nombre": "",
                                            "posiciones": []
                                        }
                                    ]
                                },
                                {
                                    "indicador": "DMI",
                                    "curvas": {
                                        "adx": [adx["ADX_14"]],
                                        "di_plus": [adx["DMP_14"]],
                                        "di_minus": [adx["DMN_14"]]
                                    }
                                },
                                {
                                    "indicador": "BollingerBands",
                                    "curvas": {
                                        "BBUp": [bbans["BBU_5_2.0"]],
                                        "BBMed": [bbans["BBM_5_2.0"]],
                                        "BBLow": [bbans["BBL_5_2.0"]]
                                    }
                                }
                            ],
                            "datos": {
                                "open":[dataToday["open"]],
                                "close":[dataToday["close"]],
                                "high":[dataToday["high"]],
                                "low":[dataToday["low"]]
                            }
                        }
                        self.MData.insert_one(jsonIndicadoresASubir)
