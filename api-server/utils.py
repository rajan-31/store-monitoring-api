from sqlalchemy.orm import Session

from .database import models, schemas
from .database.db import engine

from uuid import UUID
import pandas as pd

import datetime as dt
from zoneinfo import ZoneInfo
from timeit import default_timer as timer


def generateReport(curr_timestamp, report_id: UUID , db: Session):
    start = timer()
    db_reports_data_list = []

    store_timezones = db.query(models.StoreTimezones).all()
    menu_hours = db.query(models.MenuHours).all()
    store_status = db.query(models.StoreStatus).all()

    store_timezones = pd.DataFrame([r.__dict__ for r in store_timezones], columns=['store_id', 'timezone_str'])
    menu_hours = pd.DataFrame([r.__dict__ for r in menu_hours], columns=['store_id', 'day', 'start_time_local', 'end_time_local'])
    store_status = pd.DataFrame([r.__dict__ for r in store_status], columns=['store_id',  'status', 'timestamp_utc'])

    store_status['timestamp_utc'] = pd.to_datetime(store_status['timestamp_utc'], utc=True)

    for _sId, _sTz in store_timezones.to_numpy():
    # for _sId, _sTz in store_timezones.to_numpy()[:50]:
    # for _sId, _sTz in [store_timezones.to_numpy()[1]]:
        # print(f"{_sId}      {_sTz}\n=======================================")
    
        temp_curr_timestamp = curr_timestamp.astimezone(ZoneInfo(_sTz))
        
        last_week_start = dt.datetime.combine(temp_curr_timestamp.date() - dt.timedelta(days=7+temp_curr_timestamp.weekday()), dt.datetime.min.time()).astimezone(ZoneInfo(_sTz))
        last_week_end = dt.datetime.combine(temp_curr_timestamp.date() - dt.timedelta(days=1+temp_curr_timestamp.weekday()), dt.datetime.min.time()).astimezone(ZoneInfo(_sTz))

        last_day_date = temp_curr_timestamp.date() - dt.timedelta(days=1)

        last_hour = temp_curr_timestamp - dt.timedelta(hours = 1)
        last_hour_date = last_hour.date()
        last_hour_time = last_hour.time().hour

        # for missing data assume open 24*7
        fill_24_7 = pd.DataFrame(columns=menu_hours.columns.drop('store_id')).set_index('day')
        temp_min_time =  dt.time.min
        temp_max_time =  dt.time.max
        for i in range(7):
            fill_24_7.loc[i] = [temp_min_time, temp_max_time]

        mask = store_status['store_id'] == _sId
        _sStatus = store_status[mask].loc[:, 'status':].sort_values(by=['timestamp_utc'])

        _sStatus['timestamp_utc'] = _sStatus['timestamp_utc'].dt.tz_convert(_sTz)

        mask = menu_hours['store_id'] == _sId

        menu_hours_temp = menu_hours[mask].loc[:, 'day':].drop_duplicates(subset='day', keep='last').sort_values(by=['day']).set_index('day')
        _sMHours = menu_hours_temp if len(menu_hours_temp.index) > 0 else fill_24_7

        last_week_status = _sStatus[ (_sStatus['timestamp_utc'] >=  last_week_start) & (_sStatus['timestamp_utc'] < last_week_end)]

        last_day_status = _sStatus[ _sStatus['timestamp_utc'].dt.date ==  last_day_date]

        last_hour_status = _sStatus[ (_sStatus['timestamp_utc'].dt.date == last_hour_date) & (_sStatus['timestamp_utc'].dt.hour == last_hour_time)]

        uptime_last_hour = 0
        uptime_last_day = 0
        uptime_last_week = 0
        downtime_last_hour = 0
        downtime_last_day = 0
        downtime_last_week = 0

        _days = _sMHours.index
        
        for _status, _ts in last_week_status.to_numpy():

            if _ts.weekday() in _days:
                # status is valid: falls in menu hours range
                if _ts.time() >= _sMHours.loc[_ts.weekday()].start_time_local and _ts.time() < _sMHours.loc[_ts.weekday()].end_time_local:
                    if _status == 'active':
                        uptime_last_week+=1
                    else:
                        downtime_last_week+=1

        for _status, _ts in last_day_status.to_numpy():
            if _ts.weekday() in _days:
                if _ts.time() >= _sMHours.loc[_ts.weekday()].start_time_local and _ts.time() < _sMHours.loc[_ts.weekday()].end_time_local:
                    if _status == 'active':
                        uptime_last_day+=1
                    else:
                        downtime_last_day+=1

        if len(last_hour_status.index) != 0:
            if last_hour_status.iloc[0].status == 'active':
                uptime_last_hour = 60
            else:
                downtime_last_hour = 60

        db_reports_data_list.append(models.ReportsData(report_id=report_id, store_id=_sId, uptime_last_hour=uptime_last_hour, uptime_last_day=uptime_last_day, uptime_last_week=uptime_last_week, downtime_last_hour=downtime_last_hour, downtime_last_day=downtime_last_day, downtime_last_week=downtime_last_week))
    

    db_reports_status = db.query(models.ReportsStatus).filter(models.ReportsStatus.report_id==report_id).first()
    db_reports_status.status = 'Complete'

    db.add_all(db_reports_data_list)

    db.commit()
    db.close()

    end = timer()

    print(f'DONE REPORT: {report_id}, TIME: {end - start} seconds')