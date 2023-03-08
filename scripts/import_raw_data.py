from sqlalchemy import create_engine
import pandas as pd
import numpy as np

from dotenv import load_dotenv
import datetime as dt
from zoneinfo import ZoneInfo
import os


load_dotenv('../api-server/.env')

engine = create_engine(os.getenv('POSTGRES_URL',  ''))

# ======================================================================
# load csv files

store_timezones = pd.read_csv('../raw_data/bq-results-20230125-202210-1674678181880.csv', 
                            dtype= {'store_id': 'int64'}
                            )
menu_hours = pd.read_csv('../raw_data/Menu hours.csv', 
                        dtype= {'store_id': 'int64', 'day': 'int8'}, 
                        parse_dates=['start_time_local', 'end_time_local']
                        )
store_status = pd.read_csv('../raw_data/store status.csv', 
                        dtype={'store_id': 'int64'}, 
                        converters={'timestamp_utc': lambda str: str.replace(' UTC', '')}
                        )

# ======================================================================
# parse strings to appropriate datatypes

store_status['timestamp_utc'] = pd.to_datetime(store_status['timestamp_utc'], utc=True)
menu_hours['start_time_local'] = menu_hours['start_time_local'].dt.time
menu_hours['end_time_local'] = menu_hours['end_time_local'].dt.time

# ======================================================================

all_unique_store_id = pd.concat([store_timezones.store_id, store_status.store_id, menu_hours.store_id], ignore_index=True).unique()

# missing timezones
store_id_notIn_timezones = np.setdiff1d(all_unique_store_id, store_timezones.store_id.unique(), assume_unique=True)
temp_df = pd.DataFrame({'store_id':store_id_notIn_timezones, 'timezone_str':'America/Chicago'})

# add missing timezones
store_timezones = pd.concat([store_timezones, df_notIn_timzones])

# ======================================================================
# print datatypes and head records

print("store_timezones", store_timezones.dtypes, sep='\n', end='\n\n')
print("menu_hours", menu_hours.dtypes, sep='\n', end='\n\n')
print("store_status", store_status.dtypes, sep='\n', end='\n\n')

print("store_timezones", store_timezones.head(), sep='\n', end='\n\n')
print("menu_hours", menu_hours.head(), sep='\n', end='\n\n')
print("store_status", store_status.head(), sep='\n', end='\n\n')

# ======================================================================
# import data in database

store_timezones.to_sql('store_timezones', engine, if_exists='append', index=False)
menu_hours.to_sql('menu_hours', engine, if_exists='append', index=False)
store_status.to_sql('store_status', engine, if_exists='append', index=False)

print('Data imported successfully')