from sqlalchemy import Column, ForeignKey
from sqlalchemy import BIGINT, SMALLINT, VARCHAR, TIMESTAMP, TIME, UUID, INTEGER
from sqlalchemy.orm import relationship

from .db import Base

class StoreTimezones(Base):
    __tablename__ = 'store_timezones'

    store_id = Column(BIGINT, primary_key=True, index=True)
    timezone_str = Column(VARCHAR(100))

class StoreStatus(Base):
    __tablename__ = 'store_status'

    store_id = Column(BIGINT, primary_key=True, nullable=False, index=True)
    status = Column(VARCHAR(20))    # active/inactive
    timestamp_utc = Column(TIMESTAMP, primary_key=True)

class MenuHours(Base):
    __tablename__ = 'menu_hours'

    store_id = Column(BIGINT, primary_key=True, index=True)
    day = Column(SMALLINT, primary_key=True)  # 0 to 6
    start_time_local = Column(TIME)
    end_time_local = Column(TIME)


# Report tables

class ReportsStatus(Base):
    __tablename__ = 'reports_status'

    report_id = Column(UUID, primary_key=True, index=True)
    status = Column(VARCHAR(20))    # Running, Complete

    # data = relationship('ReportsData', back_populates='data')

class ReportsData(Base):
    __tablename__ = 'reports_data'

    report_id = Column(UUID, ForeignKey('reports_status.report_id'), primary_key=True, nullable=False, index=True)
    store_id = Column(BIGINT, primary_key=True)
    uptime_last_hour = Column(SMALLINT, nullable=False)
    uptime_last_day = Column(SMALLINT, nullable=False)
    uptime_last_week = Column(SMALLINT, nullable=False)
    downtime_last_hour = Column(SMALLINT, nullable=False)
    downtime_last_day = Column(SMALLINT, nullable=False)
    downtime_last_week = Column(SMALLINT, nullable=False)

    # status = relationship('ReportsStatus')