import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.types import Date
from sqlalchemy.sql.expression import and_, extract
from flask import Flask, jsonify


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
        f"<h1>Welcome to Stephen Lyssy's Hawaii Climate App</h1><br/><br/>"
        f"<h2> Below is a list of available routes<h2><br/>"
        """<a href="/api/v1.0/stations">/api/v1.0/stations (List of stations)</a><br/>"""
        """<a href="/api/v1.0/tobs">/api/v1.0/tobs (Temperature observations for the previous year)</a><br/>"""
        """<a href="/api/v1.0/precipitation">/api/v1.0/precipitation (Precipitation for the previous year)</a><br/>"""
        """<a href="/api/v1.0/2017-01-01/2017-12-31">/api/v1.0/start_date/end_date (Temperature statistics for given date range)</a><br/>"""
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    prcp = session.query(Measurement.date, Measurement.prcp)\
    .filter(Measurement.date >= "2016-08-23")\
    .filter(Measurement.date <= "2017-08-23")\
    .order_by(Measurement.date).all()
    
    prcp_dict = dict(prcp)
    return jsonify(prcp_dict)


@app.route("/api/v1.0/stations")
def stations():
    station = session.query(Measurement.station, 
    func.count(Measurement.id))\
    .group_by(Measurement.station)\
    .order_by(func.count(Measurement.station).desc()).all()

    station_dict = dict(station)
    return jsonify(station_dict)


@app.route("/api/v1.0/tobs")
def tobs():
    temp_obs = session.query(Measurement.station, func.count(Measurement.tobs))\
    .group_by(Measurement.station)\
    .order_by(func.count(Measurement.tobs).desc()).all()

    tobs_dict = dict(temp_obs)
    return jsonify(tobs_dict)
    



if __name__ == "__main__":
    app.run(debug=True)
