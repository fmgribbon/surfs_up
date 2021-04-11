import datetime as dt
import numpy as np
import pandas as pd

# Import SQLAlchemy dependencies

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Import Flask depencies
from flask import Flask, jsonify



# Set-up database engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect DB into classes
Base = automap_base()
Base.prepare(engine, reflect =True)

# References to Tables
Measurement = Base.classes.measurement
Station = Base.classes.station

#Session Link to DB
session = Session(engine)

# Create an app
app = Flask(__name__)

@app.route('/')


def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

# precipitation

@app.route("/api/v1.0/precipitation") 

 # calculate the date one year prior
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

   # query to get the date and precipitation for the previous year
    precipitation = session.query(Measurement.date, Measurement.prcp).\
                                    filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)                                

# Stations
#   
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)
 
# Temperature

@app.route("/api/v1.0/tobs")

def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# Temperatures

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:

        results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)
