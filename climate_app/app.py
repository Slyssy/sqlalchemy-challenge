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
    return "Welcome to my Hawaii Climate App"

@app.route("/api/v1.0/precipitation")
def precipitation():
    prcp = session.query(Measurement.date, Measurement.prcp)\
    .filter(Measurement.date >= "2016-08-23")\
    .filter(Measurement.date <= "2017-08-23")\
    .order_by(Measurement.date).all()
    
    prcp_dict = dict(prcp)
    return jsonify(prcp_dict)





# @app.route("/api/v1.0/stations")



# @app.route("/api/v1.0/tobs")





if __name__ == "__main__":
    app.run(debug=True)
