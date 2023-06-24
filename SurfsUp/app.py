# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables

Base.prepare(autoload_with=engine)
# Save references to each table
table = Base.classes.measurement
table_1=Base.classes.station

# Create our session (link) from Python to the DB

session = Session(engine)
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
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>/<end>"
       

    )
# to show the list of precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

# Calculate the date one year from the last date in data set.
    date_a_year_back = dt.date(2017, 8, 23) - dt.timedelta(days=365)

# Perform a query to retrieve the data and precipitation scores
    results = session.query(table.date,table.prcp).\
                  filter(table.date >= date_a_year_back).all()
#convert the list to dictionary
    prcp_rows = [{"Date": result[0], "Precipitation": result[1]} for result in results]

    session.close()


    return jsonify(prcp_rows)

# Return a JSON list of stations from the dataset.

@app.route("/api/v1.0/stations")
def station_names():
# Create our session (link) from Python to the DB
    session = Session(engine)
 # Query all station list
    station_list=session.query((table_1.name)).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(station_list))

    return jsonify(all_names)

# return temperature data

@app.route("/api/v1.0/tobs")
def temperatue_data():
# Create our session (link) from Python to the DB
    session = Session(engine)
# Design a query to find the most active stations (i.e. which stations have the most rows?)
    active_stations = session.query(table.station, func.count(table.station)).group_by(table.station).order_by(func.count(table.station).desc()).all()

    most_active_sation=active_stations[0][0]
# Using the most active station id
# Query the last 12 months of temperature observation data for this station
# Calculate the date one year from the last date in data set.
    date_a_year_back = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(table.tobs).filter(table.date >=date_a_year_back).filter(table.station ==most_active_sation).all()

# Convert list of tuples into normal list
    all_temp = list(np.ravel(results))

    return jsonify(all_temp)
   


if __name__ == '__main__':
    app.run(debug=True)