# import dependencies
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import datetime as dt

# Create an app, being sure to pass __name__
app = Flask(__name__)

# Set up database
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement=Base.classes.measurement
Station=Base.classes.station
session=Session(engine)

# Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f"There are all the routes you will need<br/>"
        f"Hawaii Precipitations and weather info<br/>"
        f"List of weather stations in Hawaii<br/>"
        f"Let us help you with your trip planning!<br/>"
        f"What would you like to know about?<br/>"
        f"<br/>"
        f"/precipitation<br/>"
        f"/stations<br/>"
        f"/tobs<br/>"
    )

# Define what to do when a user hits the /precipitation route
@app.route("/precipitation")
def precipitation():
    print("Server received request for 'Precipitation' page...")
    prcp_results=session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date.desc()).all()
    prcp_dict={}
    for (date, prcp) in prcp_results:
        prcp_dict.setdefault(date, []).append(prcp)
    return jsonify(prcp_dict)


# Define what to do when a user hits the /stations route
@app.route("/stations")
def stations():
    print("Server received request for 'Stations' page...")
    stations_results=session.query(func.distinct(Measurement.station)).all()
    return jsonify(stations_results)

# Define what to do when a user hits the /tobs route
@app.route("/tobs")
def tobs():
    print("Server received request for 'Temperature' page...")
    lastTwelve=session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > "2016-08-23").order_by(Measurement.date.desc()).all()
    return jsonify(lastTwelve)

@app.route("/temp/<start>")
def calc_temps_start(start):
    start_result=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    print("Server received request for '<start>' page...")
    return f"{start_result}"

@app.route("/temp/<start>/<end>")
def calc_temps(start, end):    
    print("Server received request for '<start>/<end>' page...")
    start_end_result=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    return f"{start_end_result}"

if __name__ == "__main__":
    app.run(debug=True)