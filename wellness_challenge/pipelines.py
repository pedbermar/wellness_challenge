from datetime import datetime
import calendar

def get_metrics_pipeline(metric_type, start, end):
    metrics_pipeline = [
        {   
            '$match': {
                'date': {
                    '$gt': start, 
                    '$lt': end 
                }
            }
        },
        {
            '$project': {
                'date': 1,
                metric_type: 1
            }
        },
        {
            '$sort': {
                'date': 1
            }
        }

    ]

    return metrics_pipeline

def get_current_month_pipeline():
    # Dirty date trick to get a match from the dataset
        month = datetime.now().month + 1
        year = datetime.now().year - 1
    
        # Get the number of days of the month
        m_range = calendar.monthrange(year, month)

        # 
        start = datetime(year, month, m_range[0])
        end = datetime(year, month, m_range[1])

        current_month_pipeline = [
            {
                "$match": {
                    'date': {
                        '$gt': start, 
                        '$lt': end
                    }
                }
            },
            {
                "$group": {
                    "_id": 'null', 
                    "power_avg": { '$avg': "$power" },
                    "power_factor_avg": { '$avg': "$power_factor" },
                    "energy_avg": { '$sum': "$energy" },
                    "intensity_avg": { '$avg': "$intensity" },
                    "voltage_avg": { '$avg': "$voltage" },
                    "reactive_power_avg": { '$avg': "$reactive_power" },
                    "reactive_energy_avg": { '$avg': "$reactive_energy" },

                }
            },
            {
                '$sort': {
                    'date': 1
                }
            }
        ]

        return current_month_pipeline

def get_daily_pipeline(type):
    # Dirty date trick to get a match from the dataset
    month = datetime.now().month + 1
    year = datetime.now().year - 1

    # Get the number of days of the month
    m_range = calendar.monthrange(year, month)

    # 
    start = datetime(year, month, m_range[0])
    end = datetime(year, month, m_range[1])

    daily_pipeline = [ 
        {
            "$match": {
                'date': {
                    '$gt': start, 
                    '$lt': end
                }
            }
        },
        {
            '$group': { 
                '_id' : { 
                    '$dayOfMonth': '$date'
                },
                'voltage_avg': {
                    '$avg': "$" + type 
                }
            }
        },
        {
            '$sort': {
                'date': 1
            }
        }
    ]

    return daily_pipeline