import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
import numpy as np
import pandas as pd
from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite")


Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)


app = Flask(__name__)

@app.route("/")
def index():
    return (
        f"API Paths:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start (where 'start' is a date string YYYY-MM-DD)<br/>"
        f"/api/v1.0/start/end (where 'start' and 'end' are date strings YYYY-MM-DD)<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    lastdt = session.query(func.max(Measurement.date)).scalar()
    firstdt = (dt.datetime.strptime(lastdt, "%Y-%m-%d") - dt.timedelta(365)).strftime("%Y-%m-%d")
    print(lastdt)
    print(firstdt)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= firstdt)
    precip_list = []
    for row in results:
        precip_dict = {}
        precip_dict["Date"] = row.date
        precip_dict["Precipitation"] = row.prcp
        precip_list.append(precip_dict)
    return jsonify(precip_list)
    
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.name).all()
    station_list = list(np.ravel(results))
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")    
def tobs():
    lastdt = session.query(func.max(Measurement.date)).scalar()
    firstdt = (dt.datetime.strptime(lastdt, "%Y-%m-%d") - dt.timedelta(365)).strftime("%Y-%m-%d")
    print(lastdt)
    print(firstdt)
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= firstdt)
    temp_list = []
    for row in results:
        temp_dict = {}
        temp_dict["Date"] = row.date
        temp_dict["Precipitation"] = row.tobs
        temp_list.append(temp_dict)
    return jsonify(temp_list)

@app.route("/api/v1.0/<start>")
def startdate(start):
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= start)
    precip_list = []
    for row in results:
        precip_dict = {}
        precip_dict["Date"] = row.date
        precip_dict["Precipitation"] = row.prcp
        precip_list.append(precip_dict)
    return jsonify(precip_list)

@app.route("/api/v1.0/<start>/<end>")
def daterange(start, end):
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= start, Measurement.date <= end)
    precip_list = []
    for row in results:
        precip_dict = {}
        precip_dict["Date"] = row.date
        precip_dict["Precipitation"] = row.prcp
        precip_list.append(precip_dict)
    return jsonify(precip_list)



if __name__ == '__main__':
    app.run(debug=True)