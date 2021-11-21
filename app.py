import numpy as np
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
Base.prepare(engine, reflect=True)

# Save reference to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to the Climate App!<br/><br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"(note: start = date in the form of mmddyyyy)<br/>"
        f"/api/v1.0/start/end<br/>"
        f"(note: start and end = dates in the form of mmddyyyy)"
    )

@app.route("/api/v1.0/precipitation")
def precip():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all dates and precipitation in last year of data"""
    # Query dates and precipitation of last year of data
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > dt.date(2016, 8, 22)).all()

    session.close()

    # Convert list of tuples into normal list
    all_prcp = list(np.ravel(results))

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all the stations"""
    # Query all stations
    results = session.query(Station.station, Station.name).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of dates and temps of most active station in last year of data"""
    # Query most active station's dates and temps in last year of data
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > dt.date(2016, 8, 22)).\
        filter(Measurement.station == "USC00519281").all()

    session.close()

    # Convert list of tuples into normal list
    annualMostActive = list(np.ravel(results))

    return jsonify(annualMostActive)

@app.route("/api/v1.0/<start>")
def start_date(start=""):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of min, avg, and max temps for a given start date"""
    # Query min, avg, and max temps for a given start date
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    start = dt.datetime.strptime(start, "%m%d%Y")
    results = session.query(*sel).filter(Measurement.date >= start).all()

    session.close()

    # Convert list of tuples into normal list
    start_results = list(np.ravel(results))

    return jsonify(start_results)

@app.route("/api/v1.0/<start>/<end>")
def start_and_end(start="", end=""):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of min, avg, and max temps for between given start and end dates"""
    # Query min, avg, and max temps for between given start and end dates
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    start = dt.datetime.strptime(start, "%m%d%Y")
    end = dt.datetime.strptime(end, "%m%d%Y")
    results = session.query(*sel).filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    session.close()

    # Convert list of tuples into normal list
    start_and_end_results = list(np.ravel(results))

    return jsonify(start_and_end_results)


if __name__ == '__main__':
    app.run(debug=True)