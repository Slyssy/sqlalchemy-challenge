import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.types import Date
from sqlalchemy.sql.expression import and_, extract
from flask import Flask, jsonify
import numpy as np


base = declarative_base()

class Measurement(base):
    __tablename__ = "measurement"
    id = Column(Integer, primary_key=True)
    station = Column(String)
    date  = Column(String)
    prcp  = Column(Float)
    tobs  = Column(Float)

class Station(base):
    __tablename__ = "station"
    id = Column(Integer, primary_key=True)
    station = Column(String)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    elevation = Column(Float)
    
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")
conn = engine.connect()
session = Session(bind=engine)

app = Flask(__name__)


# session = Session(bind=engine)

@app.route("/")
def home():
    return (
        f"<h1>Welcome to Stephen Lyssy's Hawaii Climate App</h1><br/>"
        f"<h2>Below is a list of available routes<h2>"
        f"<h4>(You must refresh page everytime you return in order to use the links)</h4><br/>"
        f"<h4>Final year in data's Precipitation Measurements:</h4>"
        """<a href="/api/v1.0/precipitation">/api/v1.0/precipitation </a><br/>"""        
        f"<h4>Most Active stations:</h4>"
        """<a href="/api/v1.0/stations">/api/v1.0/stations</a><br/>"""
        f"<h4>Temperature observations for most active weather station from the final year's data:</h4>"
        """<a href="/api/v1.0/tobs">/api/v1.0/tobs </a><br/>"""
        f"<h4>Temperature statistics for final year's data for my vacation dates (start/end dates):<h4>"
        f"<h6>**Note: If you only enter a start date, statistical data will be for dates greater than or equal to the start date you selected (default is my vaction dates):<h4>"
        """Start: <a href="/api/v1.0/2017-02-13">/api/v1.0/start_date</a><br/>"""
        """Start/End: <a href="/api/v1.0/2017-02-13/2017-02-23">/api/v1.0/start_date/end_date</a><br/>"""
    )
# Returns JSON dict of the final year's precipitation data.
@app.route("/api/v1.0/precipitation")
def precipitation():
    prcp = session.query(Measurement.date, Measurement.prcp)\
    .filter(Measurement.date >= "2016-08-23")\
    .filter(Measurement.date <= "2017-08-23")\
    .order_by(Measurement.date).all()
    
    # prcp_dict = dict(prcp)
    prcp_dict = {date: precipitation for date, precipitation in prcp}

    return jsonify(prcp_dict)

# Returns a JSON list of the most active stations.
@app.route("/api/v1.0/stations")
def stations():
    station = session.query(Measurement.station, 
    func.count(Measurement.id))\
    .group_by(Measurement.station)\
    .order_by(func.count(Measurement.station).desc()).all()

    station_list = list(station)
    return jsonify(station_list)

# Returns a JSON list of temperature observations (TOBS) for the previous year for the most active weather station.
@app.route("/api/v1.0/tobs")
def tobs():
    temp_obs = session.query(Measurement.date, Measurement.tobs)\
    .filter(Measurement.station=="USC00519281")\
    .filter(
    and_(Measurement.date >= "2016-08-23", Measurement.date <= "2017-08-23")).all()

    tobs_list = list(temp_obs)
    return jsonify(tobs_list)

# Returns a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def start_date(start, end=None):

    q = session.query(str(func.min(Measurement.tobs)), str(func.avg(Measurement.tobs)), str(func.max(Measurement.tobs)))
    
    if start:
        q = q.filter(Measurement.date >= start)

    if end:
        q = q.filter(Measurement.date <= end)

    results =q.all()[0]

    results = list(results)
    return jsonify(results)

# I have this commented out, but this actually looks nicer. This return a JSON dict.
# The homework ask to return a JSON list.

    # keys = ["Min_Temp", "Max_Temp", "Avg_Temp"]

    # tobs_dict = {keys[i]: results[i] for i in range(len(keys))}

    # return jsonify(tobs_dict)
   

    
  
    # I left this here because this was another way I discovered to create a JSON list, and I wanted to save this code.  
# @app.route("/api/v1.0/temps/<start>")
# def temp_start(start=None):
    
#     start_temps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
#     filter(Measurement.date >= start).all()

#     start_temps = list(np.ravel(start_temps))
#     return jsonify(start_temps)
    
    
if __name__ == "__main__":
    app.run(debug=True)
