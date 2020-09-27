from keras.utils import np_utils
from tqdm import *
from datetime import datetime, timedelta

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

import Herramientas as tools
import Indicadores as indicator


class MyModel(tf.keras.Model):

    def __init__(self):
        super(MyModel, self).__init__()
        self.dense1 = tf.keras.layers.Dense(32, input_dim=2100, activation=tf.nn.relu)
        self.dense2 = tf.keras.layers.Dense(100, activation=tf.nn.softmax)
        self.dropout = tf.keras.layers.Dropout(0.5)

    def call(self, inputs):
        x = self.dense1(inputs)
        return self.dense2(x)


class IA:
    cedears = []

    def __init__(self, cedearsList):
        self.cedears = cedearsList


    def comparation(self, firstNumber, secondNumber):
        if secondNumber > firstNumber - 5 and secondNumber < firstNumber:
            return 3
        elif secondNumber > firstNumber - 10 and secondNumber <= firstNumber - 5:
            return 2
        elif secondNumber > firstNumber - 20 and secondNumber <= firstNumber - 10:
            return 1
        elif secondNumber <= firstNumber - 20:
            return 0

        if secondNumber < firstNumber + 5 and secondNumber >= firstNumber:
            return 4
        elif secondNumber < firstNumber + 10 and secondNumber >= firstNumber + 5:
            return 5
        elif secondNumber < firstNumber + 20 and secondNumber >= firstNumber + 10:
            return 6
        elif secondNumber >= firstNumber + 20:
            return 7


    def createTrainsDataCedears(self, dateToStart):
        DAYS = 30

        date_time = datetime.fromisoformat(dateToStart)
        xTrains = []
        yTrains = []
        yTest = []
        xTest = []
        trainOrTest = True
        for NroCedear in tqdm(range(30)):
            if NroCedear == 27:
                continue
            cedearTicket = self.cedears[NroCedear]
            prom = tools.getInfoFewDaysAgo(1, date_time + timedelta(days=1), cedearTicket, 10)
            if type(prom) != type("") :
                prom = [prom["open"][0], prom["close"][0], prom["high"][0], prom["low"][0]]
                prom = np.mean(prom)
                data = tools.getInfoFewDaysAgo(DAYS, date_time, cedearTicket, 10)
                Bands = indicator.getBollingerBands(data)
                xQuantity = Bands.size
                heatMap = np.zeros((100, xQuantity))
                for xPos in range(5, xQuantity):
                    yPos = tools.acotation(np.max(data['high']), np.min(data['low']), Bands['BBM_5_2.0'][xPos])
                    yPosClose = tools.acotation(np.max(data['high']), np.min(data['low']), data['close'][xPos])
                    yPosOpen = tools.acotation(np.max(data['high']), np.min(data['low']), data['open'][xPos])
                    if yPos >= 100:
                        yPos = 99
                    if yPosClose >= 100:
                        yPosClose = 99
                    if yPosOpen >= 100:
                        yPosOpen = 99

                    if yPosOpen < yPosClose:
                        heat = 100
                        plus = 80 / (yPosClose - yPosOpen)
                        for y in range(yPosOpen, yPosClose):
                            heatMap[y][xPos] = int(heat)
                            heat += plus
                    elif yPosClose < yPosOpen:
                        heat = 180
                        substrac = 80 / (yPosOpen - yPosClose)
                        for y in range(yPosClose, yPosOpen):
                            heatMap[y][xPos] = int(heat)
                            heat -= substrac
                    heatMap[yPos][xPos] = 255
                acotationVar = tools.acotation(np.max(data["high"]), np.min(data["low"]), prom)
                if acotationVar >= 100:
                    acotationVar = 99
                elif acotationVar < 0:
                    acotationVar = 0
                if trainOrTest:
                    yTrains.append(acotationVar)
                    xTrains.append(heatMap.copy())
                else:
                    yTest.append(acotationVar)
                    xTest.append(heatMap.copy())
                trainOrTest = not trainOrTest
                plt.imshow(heatMap, cmap='hot', interpolation='nearest')
                plt.show()
        xTrains = np.array(xTrains)
        yTrains = np.array(yTrains)
        xTest = np.array(xTest)
        yTest = np.array(yTest)

        return xTrains, yTrains, xTest, yTest

    def runIATest(self):
        xTrains, yTrains, xTest, yTest = self.createTrainsDataCedears("2020-08-26")

        # adapt the data
        xTrains = xTrains.reshape((xTrains.shape[0], xTrains.shape[1] * xTrains.shape[2]))
        xTest = xTest.reshape((xTest.shape[0], xTest.shape[1] * xTest.shape[2]))

        xTrains = xTrains / 255
        xTest = xTest / 255

        yTrains = np_utils.to_categorical(yTrains, 100)
        yTest = np_utils.to_categorical(yTest, 100)

        # use the model

        model = MyModel()

        model.compile(optimizer='sgd', loss='categorical_crossentropy', metrics=['accuracy'])

        model.fit(x=xTrains, y=yTrains, batch_size=100, epochs=10, verbose=1, validation_data=(xTest, yTest))

        evaluacion = model.evaluate(x=xTest, y=yTest, batch_size=100, verbose=1)

        print(yTest)
        print(evaluacion)
