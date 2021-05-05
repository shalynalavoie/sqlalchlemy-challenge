import numpy as np 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#Database setup
engine = create_engine("sqlite:///resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect= True)
#Save references to each table
Base.classes.keys()
Measurement = Base.classes.measurement
Station = Base.classes.station

#Create session from Python to DB
session = Session(engine)

#Flask Setup
app = Flask(__name__)

#Flask routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Let's look into the precipitation data."""
    precip_results = session.query(Measurement.date, Measurement.prcp).all()
    return jsonify(precip_results)

@app.route("/api/v1.0/stations")
def station():
     stat_results + session.query(Station.station, Station.name).all()
     return jsonify(stat_results)


@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for tobs...")

    # query temperature readings for last year, based on start date calculated earlier in notebook
    tobs_results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == station_most_active).\
        filter(Measurement.date >= start_date).all()

      # convert to a dataframe
    tobs_df = pd.DataFrame(tobs_results, columns=["Date", "Tobs"]).set_index("Date")
    tobs_df = tobs_df.sort_values("Date")
    tobs_dict = tobs_df.T.to_dict()

    return jsonify(tobs_dict)


    # show aggregate temperature data from a user-defined start date in URL,
# by calling provided function with an end date of 9999-12-31.  May have to revisit
# this approach in ~8000 years.
@app.route("/api/v1.0/<start>")
def start_temps(start):

    temp_results = calc_temps(start, "9999-12-01")

    temp_df = pd.DataFrame(temp_results, columns=["TMin", "TAvg", "TMax"])
    temp_dict = temp_df.T.to_dict()

    return jsonify(temp_dict)

# show aggregate temperature data from a user-defined start date 
# and end date in URL, by calling provided function
@app.route("/api/v1.0/<start>/<end>")
def start_end_temps(start, end):

    temp_results = calc_temps(start, end)

    temp_df = pd.DataFrame(temp_results, columns=["TMin", "TAvg", "TMax"])
    temp_dict = temp_df.T.to_dict()

    return jsonify(temp_dict)

# run the flask page
if __name__ == "__main__":
    app.run(debug=True)             