from flask import Flask, Response, json
from pymongo import *
from datetime import datetime, timedelta
from bson.json_util import dumps

app = Flask(__name__)
myclient = MongoClient("mongodb://localhost:27017/")


mydb = myclient["Market"]
mycol = mydb["ticketsCedears"]
myData = mydb["cedearData"]
myOtherData = mydb["cedearPureData"]


@app.route('/')
def base():
    return Response(response=json.dumps({"Status": "UP"}),
                    status=200,
                    mimetype='application/json')


@app.route('/cedearsToday', methods=['GET'])
def cedearsToday():
    response = dumps(myOtherData.find({"fecha": datetime.now().strftime("%m/%d/%Y")}))
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='127.0.0.1')