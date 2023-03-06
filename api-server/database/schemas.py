from pydantic import BaseModel, UUID4
from datetime import datetime, time

class storeTimezonesBase(BaseModel):
    store_id: int
    timezone_str: str

class storeStatusBase(BaseModel):
    store_id: int
    status: str
    timestamp_utc: datetime

class MenuHoursBase(BaseModel):
    store_id: int
    day: int
    start_time_local: time
    end_time_local: time


# Report schemas

class ReportsStatusBase(BaseModel):
    report_id: UUID4
    status: str

class ReportsDataBase(BaseModel):
    report_id: UUID4
    store_id: int
    uptime_last_hour: int
    uptime_last_day: int
    uptime_last_week: int
    downtime_last_hour: int
    downtime_last_day: int
    downtime_last_week: int