from datetime import timedelta
from yahoo_fin.stock_info import *


def acotation(max, min, num):
    if (max - min) < 1:
        return int(((num - min) / 1) * 99)
    return int(((num - min) / (max - min)) * 99)

def getInfoFewDaysAgo(days, actualDate, ticket, tolerance):
    try:
        data = ""
        size = 0
        toleranceNro = 0
        laboralDays = days
        while (size != days and toleranceNro != tolerance):
            date_N_days_ago = actualDate - timedelta(days=laboralDays)
            dateInStringStart = date_N_days_ago.strftime("%m/%d/%Y")
            dateInStringEnd = actualDate.strftime("%m/%d/%Y")
            data = get_data(ticket, start_date=dateInStringStart,end_date=dateInStringEnd)
            size = data["high"].size
            if (size != days):
                toleranceNro += 1
                laboralDays += 1
        return data
    except:
        return "failure"