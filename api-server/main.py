from fastapi import FastAPI, Response
from fastapi import Depends, HTTPException, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from dotenv import load_dotenv
import os
from uuid import uuid4, UUID
import datetime as dt
from zoneinfo import ZoneInfo
import csv
import io

from . import crud
from . import utils
from .database.db import SessionLocal, engine
from .database import models, schemas


''' Create tables if does not exists using models '''
# models.Base.metadata.create_all(bind=engine)

load_dotenv()

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Hello World!"}

@app.get("/trigger_report")
async def trigger_report(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    report_id = uuid4()

    curr_timestamp = dt.datetime(2023, 1, 25, 20, 0, 0, 0, tzinfo=ZoneInfo('Asia/Kolkata'))
    background_tasks.add_task(utils.generateReport, curr_timestamp, report_id, db)

    return crud.create_report(db=db, report_id=report_id, status='Running')

@app.get("/get_report/{report_id}")
async def get_report( report_id: str, db: Session = Depends(get_db)):

    try:
        db_report_status = crud.get_report_status(db=db, report_id=UUID(report_id))
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid report id")

    if not db_report_status:
        raise HTTPException(status_code=400, detail="Invalid report id")
    if db_report_status.status == 'Running':
        return { 'status': 'Running' }
    else:
        data = [row.tuple() for row in crud.get_report_data(db=db, report_id=UUID(report_id))]
        labels = ['store_id', 'uptime_last_hour', 'uptime_last_day', 'uptime_last_week', 'downtime_last_hour', 'downtime_last_day', 'downtime_last_week']

        output = io.StringIO()

        writer = csv.writer(output)
        writer.writerow(labels)
        
        for row in data:
            writer.writerow(row)

        csv_string = output.getvalue()

        return {
            'csv_string': csv_string,
            'status': 'Complete'
        }