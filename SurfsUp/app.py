# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
station = Base.classes.station
measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route('/')
def welcome():
    return (
        f"Welcome!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )


@app.route('/api/v1.0/precipitation')
def precip():
    year_prcp = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= '2016-08-23').\
        order_by(measurement.date).all()
    prcp_dict = dict(row for row in year_prcp)

    return jsonify(prcp_dict)


@app.route('/api/v1.0/stations')
def stations():
    station_names = session.query(station.station).all()

    station_list = [row[0] for row in station_names]
    
    return jsonify(station_list)


@app.route('/api/v1.0/tobs')
def tobs():
    year_temp = session.query(measurement.date, measurement.tobs).\
        filter(measurement.station == 'USC00519281').\
        filter(measurement.date >= '2016-08-23').all()
    
    temp_list = [row[1] for row in year_temp]
    return jsonify(temp_list)


@app.route('/api/v1.0/<start>')
def temp_start(start):
    TMIN = session.query(func.min(measurement.tobs)).filter(measurement.date >= start).all()
    TMAX = session.query(func.max(measurement.tobs)).filter(measurement.date >= start).all()
    TAVG = session.query(func.avg(measurement.tobs)).filter(measurement.date >= start).all()
    temp_stats = [TMIN[0][0], TMAX[0][0], TAVG[0][0]]
    return jsonify(temp_stats)

@app.route('/api/v1.0/<start>/<end>')
def temp_start_end(start, end):
    if start < end:
        TMIN = session.query(func.min(measurement.tobs)).filter(measurement.date >= start).\
            filter(measurement.date <= end).all()
        TMAX = session.query(func.max(measurement.tobs)).filter(measurement.date >= start).\
            filter(measurement.date <= end).all()
        TAVG = session.query(func.avg(measurement.tobs)).filter(measurement.date >= start).\
            filter(measurement.date <= end).all()
        temp_stats = [TMIN[0][0], TMAX[0][0], TAVG[0][0]]
        return jsonify(temp_stats)
    
    return jsonify({'error': 'invalid dates. start date much be less than end date'})
    

if __name__ == "__main__":
    app.run(debug=True)