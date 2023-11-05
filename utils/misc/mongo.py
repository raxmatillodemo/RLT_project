from pymongo import MongoClient
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


client = MongoClient('mongodb+srv://raxmatillo:adminR2023@raxmatillo.wrvj1xg.mongodb.net/test?retryWrites=true&w=majority')

db = client.sample

collection = db.sample_collection



def get_values(start_date, end_date):
    result = collection.find({"dt": {"$gte": start_date, "$lte": end_date}})
    daily_values = 0
    for document in result:
        daily_values += document["value"]
    return daily_values




def month_func(start_date, end_date):
    difference = relativedelta(end_date, start_date)
    num_of_months = difference.months + (difference.years * 12)

    data = {
        "dataset": list(),
        "labels": list(),
    }

    index = 0
    for n in range(0, num_of_months+1):
        
        first_day = (start_date + relativedelta(months=n)).replace(day=1)
        last_day_of_last_month = (end_date - relativedelta(months=num_of_months-index, days=0)).replace(hour=23, minute=59, second=59)
  
        value = get_values(first_day, last_day_of_last_month)

        data["labels"].append(first_day.strftime('%Y-%m-%d %H:%M:%S'))
        data["dataset"].append(value)

        index+=1
        
    return data


def day_func(start_date, end_date):
    day_n = end_date - start_date
    day_n = abs(day_n.days)+1

    data = {
        "dataset": list(),
        "labels": list(),
    }

    for n in range(0, day_n):
        
        start_n_time = timedelta(days=n, hours=0, minutes=0, seconds=0)
        ss_date = start_date+start_n_time

        end_n_time = timedelta(days=n, hours=23, minutes=59, seconds=59)
        ee_date = start_date+end_n_time
        
        data["labels"].append(ss_date.strftime('%Y-%m-%d %H:%M:%S'))
        value = get_values(ss_date, ee_date)
        data["dataset"].append(value)
        
    return data



def hour_func(start_date, end_date):
    day_n = end_date - start_date
    day_n = abs(day_n.days*60)+1

    data = {
        "dataset": list(),
        "labels": list(),
    }

    for n in range(0, day_n):
        
        start_n_time = timedelta(hours=n, minutes=0, seconds=0)
        ss_date = start_date+start_n_time

        end_n_time = timedelta(hours=n, minutes=59, seconds=59)
        ee_date = start_date+end_n_time
        
        data["labels"].append(ss_date.strftime('%Y-%m-%d %H:%M:%S'))
        value = get_values(ss_date, ee_date)
        data["dataset"].append(value)
        
    return data




def querResult(query):
    try:
        start = query["dt_from"]
        end = query["dt_upto"]
    except Exception as err:
            return """Невалидный запос. Пример запроса: {"dt_from": "2022-09-01T00:00:00", "dt_upto": "2022-12-31T23:59:00", "group_type": "month"}"""
 
    start_date = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
    end_date = datetime.strptime(end, "%Y-%m-%dT%H:%M:%S")
    

    if query["group_type"] == "month": return month_func(start_date, end_date)
    elif query["group_type"] == "day": return day_func(start_date, end_date)
    elif query["group_type"] == "hour": return hour_func(start_date, end_date)
    
