from pyramid.view import view_config
import csv
import json
import pandas as pd
import sys, getopt, pprint
from pymongo import MongoClient
from datetime import datetime
from bson.json_util import dumps
from pyramid.httpexceptions import HTTPFound
from .security import USERS, check_password
from .pipelines import get_current_month_pipeline, get_daily_pipeline, get_metrics_pipeline


csvfilepath = './bin/report.csv'

@view_config(route_name='index', renderer='json')
def index(request):
    return {
        'project': 'Wellness Challenge',
        'author': 'Pedro Berrocal',
        'email': 'pedbermar@gmail.com'
    }


@view_config(route_name='load_csv', renderer='json')
def load_csv(request):

    db = request.db.wellness_challenge

    db.drop()
    reader = csv.DictReader( csvfilepath )         
        
    with open(csvfilepath, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        header = next(reader)
        
        header_map = {
            "Date": 'date',
            "Energy (kWh)": 'energy',
            "Reactive energy (kVArh)": 'reactive_energy',
            "Power (kW)": 'power', 
            "Maximeter (kW)": 'maximeter',
            "Reactive power (kVAr)": 'reactive_power',
            "Voltage (V)": 'voltage', 
            "Intensity (A)": 'intensity', 
            "Power factor (o)": 'power_factor'
        }
        
        for each in reader:

            row={}
            for field in header:
                if field == 'Date':
                    date = datetime.strptime(each[field], "%d %b %Y %H:%M:%S")
                    row[header_map[field]] = date
                else:
                    row[header_map[field]] = float(each[field]) if each[field] != '' else 0.0

            db.insert(row)
    
    return {'INFO':'Success loading CSV to MongoDB'}


@view_config(route_name='metrics', renderer='json')
def metrics(request):

    db = request.db.wellness_challenge

    metric_type = request.matchdict['type']
    start = datetime.strptime(request.matchdict['startDate'], '%Y%m%d%H%M%S')
    end = datetime.strptime(request.matchdict['endDate'], '%Y%m%d%H%M%S')
    
    metrics_pipeline = get_metrics_pipeline(metric_type, start, end)
    metrics = db.aggregate(metrics_pipeline)

    result = []
    for obj in metrics:
        dt = obj['date']
        time_str = dt.isoformat()
        metric = obj[metric_type]
        result.append(
            {
                'date': time_str, 
                metric_type: metric
            }
        )
    
    return result


@view_config(route_name='current_month', renderer='json')
def current_month(request):

        db = request.db.wellness_challenge

        current_month_pipeline = get_current_month_pipeline()
        metrics = request.db.wellness_challenge.aggregate(current_month_pipeline)

        metrics_avg = []
        for m in metrics:
            metrics_avg = {
                'energy': m['energy_avg'],
                'reactive_energy': m['reactive_energy_avg'],
                'power': m['power_avg'], 
                'voltage': m['voltage_avg'], 
                'intensity': m['intensity_avg'], 
                'power_factor': m['power_factor_avg']
            }

        return metrics_avg


@view_config(route_name='daily', renderer='json')
def daily(request):
    db = request.db.wellness_challenge

    daily_pipeline = get_daily_pipeline(request.matchdict['type'])

    daily_avg = request.db.wellness_challenge.aggregate(daily_pipeline)

    bucket = []
    for m in daily_avg:
        date = datetime(datetime.now().year - 1, datetime.now().month + 1, m['_id'])

        bucket.append({
            'date': date.isoformat(),
            'voltage': m['voltage_avg'], 
        })

    return bucket

@view_config(route_name='login', renderer='json')
def login(request):
    login = request.params['login']
    password = request.params['password']
    hashed_pw = USERS.get(login)
    if hashed_pw and check_password(password, hashed_pw):
        return {'token': request.create_jwt_token(login)}
    else:
        return {'ERROR': 'Login Failed'}