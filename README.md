from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import datetime
import os

dates = []

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../Resources/hawaii.sqlite"

db = SQLAlchemy(app)

class Measurement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    station = db.Column(db.String(30))
    date  = db.Column(db.String(30))
    prcp  = db.Column(db.Float)
    tobs  = db.Column(db.Float)

    def to_dict(self):
        return {
            column.name: getattr(self, column.name)
            if not isinstance(
                getattr(self, column.name), (datetime.datetime, datetime.date)
            )
            else getattr(self, column.name).isoformat()
            for column in self.__table__.columns
        }

class Station(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    station = db.Column(db.String(30))
    name = db.Column(db.String(30))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    elevation = db.Column(db.Float)

db.create_all()

# session = Session(bind=engine)

@app.route("/")
def home():
    return "Welcome to my Hawaii Climate App"

@app.route("/api/v1.0/precipitation")
def precipitation():
    prcp = db.query(Measurement.date, Measurement.prcp)\
    .filter(Measurement.date >= "2016-08-23")\
    .filter(Measurement.date <= "2017-08-23")\
    .order_by(Measurement.date).all()
    
    return jsonify([Measurement.to_dict for date in dates])




# @app.route("/api/v1.0/stations")



# @app.route("/api/v1.0/tobs")





if __name__ == "__main__":
    app.run(debug=True)
