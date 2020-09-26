import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go


def getStochasticIndicator(data):
    stoch = ta.stoch(data["high"], data["low"], data["close"])
    return stoch


def getADXIndicator(data):
    adx = ta.adx(data["high"], data["low"], data["close"])
    return adx

def getBollingerBands(data):
    bband = ta.bbands(data["close"])
    return bband

def getStochasticToday(data):
    stoch = getStochasticIndicator(data)
    result = stoch.iloc[-1]
    return result

def getADXToday(data):
    adx = getADXIndicator(data)
    result = adx.iloc[-1]
    return result

def getBollingerBandsToday(data):
    bbands = getBollingerBands(data)
    result = bbands.iloc[-1]
    return result

def showStochGraphic(stochData, ticket):
    dateStoch = stochData.index.values
    newDateStoch = []
    for date in dateStoch:
        newDate = pd.to_datetime(str(date))
        newDate = newDate.strftime("%Y-%m-%d")
        newDateStoch.append(newDate)
    print(newDateStoch)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=newDateStoch, y=stochData["STOCHFk_14"],
                        mode='lines+markers',
                        name='STOCHFk_14'))
    fig.add_trace(go.Scatter(x=newDateStoch, y=stochData["STOCHFd_3"],
                        mode='lines+markers',
                        name='STOCHFd_3'))
    fig.add_trace(go.Scatter(x=newDateStoch, y=stochData["STOCHk_5"],
                        mode='lines+markers',
                        name='STOCHk_5'))
    fig.add_trace(go.Scatter(x=newDateStoch, y=stochData["STOCHd_3"],
                        mode='lines+markers',
                        name='STOCHd_3'))
    annotations = [(dict(xref='paper', yref='paper', x=0.0, y=1.05,
                                  xanchor='left', yanchor='bottom',
                                  text=ticket,
                                  font=dict(family='Arial',
                                            size=30,
                                            color='rgb(37,37,37)'),
                                  showarrow=False))]
    fig.update_layout(annotations=annotations)
    fig.show()

def showADXGraphic(adxData, ticket):
    dateAdx = adxData.index.values
    newDateAdx = []
    for date in dateAdx:
        newDate = pd.to_datetime(str(date))
        newDate = newDate.strftime("%Y-%m-%d")
        newDateAdx.append(newDate)
    print(newDateAdx)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=newDateAdx, y=adxData["ADX_14"],
                        mode='lines+markers',
                        name='ADX_14'))
    fig.add_trace(go.Scatter(x=newDateAdx, y=adxData["DMP_14"],
                        mode='lines+markers',
                        name='DMP_14'))
    fig.add_trace(go.Scatter(x=newDateAdx, y=adxData["DMN_14"],
                        mode='lines+markers',
                        name='DMN_14'))
    annotations = [(dict(xref='paper', yref='paper', x=0.0, y=1.05,
                                  xanchor='left', yanchor='bottom',
                                  text=ticket,
                                  font=dict(family='Arial',
                                            size=30,
                                            color='rgb(37,37,37)'),
                                  showarrow=False))]
    fig.update_layout(annotations=annotations)
    fig.show()

def showBBGraphic(bollingerData, data, ticket):
    dateBollinger = data.index.values
    newDateBollinger = []
    for date in dateBollinger:
        newDate = pd.to_datetime(str(date))
        newDate = newDate.strftime("%Y-%m-%d")
        newDateBollinger.append(newDate)
    print(newDateBollinger)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=newDateBollinger, y=bollingerData["BBU_5_2.0"],
                        mode='lines+markers',
                        name='BBU_5_2.0'))
    fig.add_trace(go.Scatter(x=newDateBollinger, y=bollingerData["BBM_5_2.0"],
                        mode='lines+markers',
                        name='BBM_5_2.0'))
    fig.add_trace(go.Scatter(x=newDateBollinger, y=bollingerData["BBL_5_2.0"],
                        mode='lines+markers',
                        name='BBL_5_2.0'))
    fig.add_trace(go.Candlestick(x=newDateBollinger,
                           open=data['open'],
                           high=data['high'],
                           low=data['low'],
                           close=data['close']))
    annotations = [(dict(xref='paper', yref='paper', x=0.0, y=1.05,
                                  xanchor='left', yanchor='bottom',
                                  text=ticket,
                                  font=dict(family='Arial',
                                            size=30,
                                            color='rgb(37,37,37)'),
                                  showarrow=False))]
    fig.update_layout(annotations=annotations)
    fig.show()