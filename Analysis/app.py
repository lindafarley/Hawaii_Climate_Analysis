import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import json

# Create engine using the `demographics.sqlite` database file
engine = create_engine("sqlite:///hawaii.db")

# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(engine, reflect=True)

measurement_table = Base.classes.measurement
station_table = Base.classes.station 

session=Session(bind=engine)

app = Flask(__name__)

#Define welcome route
@app.route("/")
def welcome():
  return (
      f"Available Routes:<br/>"
      f"/api/v1.0/precipitation<br/>"
      f"/api/v1.0/stations<br/>"
      f"/api/v1.0/tobs<br/>"
      f"/api/v1.0/<start><br/>"
      f"/api/v1.0/<start>/<end>"
  )

#Define precipitation route
@app.route("/api/v1.0/precipitation")
def prcp():
    engine = create_engine("sqlite:///hawaii.db")
    prcp_query = pd.read_sql_query("SELECT date,prcp FROM measurement_sql WHERE date between '2017-01-01' AND '2018-01-01';", engine)
    # Create a dictionary from the query data
    prcp_dict = list(prcp_query.set_index('date').to_dict().values()).pop()

    return jsonify(prcp_dict)

#Define station route
@app.route("/api/v1.0/stations")
def stations():
    engine = create_engine("sqlite:///hawaii.db")
    active_query = pd.read_sql_query("SELECT station,SUM(tobs) FROM measurement_sql GROUP BY station ORDER BY tobs DESC", engine)
    #Convert to json string
    active_query = active_query.to_json()
    #Convert to dictionary
    station_dict = json.loads(active_query)
    return jsonify(station_dict["station"])


#Define tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    engine = create_engine("sqlite:///hawaii.db")
    temp_queryAll = pd.read_sql_query("SELECT date,tobs FROM measurement_sql WHERE date between '2017-01-01' AND '2018-01-01'", engine)
    #Convert to json string
    temp_queryAll = temp_queryAll.to_json()
    #Convert to dictionary
    temp_dict = json.loads(temp_queryAll)
    return jsonify(temp_dict)


#Define start route
@app.route("/api/v1.0/<start_date>")
def start(start_date):
    engine = create_engine("sqlite:///hawaii.db")
    start_query = pd.read_sql_query("SELECT min(tobs),avg(tobs),max(tobs) FROM measurement_sql WHERE date >= '" + start_date + "'", engine)
    #Convert to json string
    start_query = start_query.to_json()
    #Convert to dictionary
    start_dict = json.loads(start_query)
    return jsonify(start_dict)

#Define start-end route
@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end(start_date, end_date):
    engine = create_engine("sqlite:///hawaii.db")
    end_query = pd.read_sql_query("SELECT min(tobs),avg(tobs),max(tobs) FROM measurement_sql WHERE date between '" + start_date + "' AND '" + end_date +"'", engine)
    #Convert to json string
    end_query = end_query.to_json()
    #Convert to dictionary
    end_dict = json.loads(end_query)
    return jsonify(end_dict)

if __name__ == '__main__':
    app.run(debug=True)

      
      
      
      
      
      
      
      
      
      
      
      
     