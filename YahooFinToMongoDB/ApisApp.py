from flask import Flask, Response, request, json
from pymongo import *
from bson.json_util import dumps
from BaseDeDatos import BaseDeDatos
import json

MyBase = BaseDeDatos("mongodb://localhost:27017/", "Market", "ticketsCedears", "cedearPureData")

app = Flask(__name__)


@app.route('/')
def base():
    return Response(response=json.dumps({"Status": "UP"}),
                    status=200,
                    mimetype='application/json')


@app.route('/action', methods=['GET'])
def actions():
    response = dumps(MyBase.MData.find({"ticket": request.args["ticket"]}))
    return Response(response=response,
                    status=200,
                    mimetype='application/json')

@app.route('/actionBetweenDates', methods=['GET'])
def actionsBetweenDates():
    archivo = dumps(MyBase.MData.find({"ticket": request.args["ticket"]}))
    archivo = json.loads(archivo)
    posFechaInicio = archivo[0]["fechas"].index(request.args["dateStart"])
    posFechaFin = (archivo[0]["fechas"].index(request.args["dateEnd"])) + 1
    archivo[0]["fechas"] = archivo[0]["fechas"][posFechaInicio:posFechaFin]

    archivo[0]["indicadores"][0]["curvas"]["slowk"] = archivo[0]["indicadores"][0]["curvas"]["slowk"][posFechaInicio:posFechaFin]
    archivo[0]["indicadores"][0]["curvas"]["slowd"] = archivo[0]["indicadores"][0]["curvas"]["slowd"][posFechaInicio:posFechaFin]

    archivo[0]["indicadores"][1]["curvas"]["adx"] = archivo[0]["indicadores"][1]["curvas"]["adx"][posFechaInicio:posFechaFin]
    archivo[0]["indicadores"][1]["curvas"]["di_plus"] = archivo[0]["indicadores"][1]["curvas"]["di_plus"][posFechaInicio:posFechaFin]
    archivo[0]["indicadores"][1]["curvas"]["di_minus"] = archivo[0]["indicadores"][1]["curvas"]["di_minus"][posFechaInicio:posFechaFin]

    archivo[0]["indicadores"][2]["curvas"]["BBUp"] = archivo[0]["indicadores"][2]["curvas"]["BBUp"][posFechaInicio:posFechaFin]
    archivo[0]["indicadores"][2]["curvas"]["BBMed"] = archivo[0]["indicadores"][2]["curvas"]["BBMed"][posFechaInicio:posFechaFin]
    archivo[0]["indicadores"][2]["curvas"]["BBLow"] = archivo[0]["indicadores"][2]["curvas"]["BBLow"][posFechaInicio:posFechaFin]

    archivo[0]["datos"]["open"] = archivo[0]["datos"]["open"][posFechaInicio:posFechaFin]
    archivo[0]["datos"]["close"] = archivo[0]["datos"]["close"][posFechaInicio:posFechaFin]
    archivo[0]["datos"]["high"] = archivo[0]["datos"]["high"][posFechaInicio:posFechaFin]
    archivo[0]["datos"]["low"] = archivo[0]["datos"]["low"][posFechaInicio:posFechaFin]

    response = dumps(archivo)
    return Response(response=response,
                    status=200,
                    mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='127.0.0.1')