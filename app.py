from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask
import json

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
db = automap_base()
# reflect the tables
db.prepare(engine,reflect = True)

# Save references to each table
Station = db.classes.station
Measurement = db.classes.measurement
app = Flask(__name__)

# 1st route homepage
@app.route("/")
def homepage():
    message = """

Home page.<br/>
Routes that are available.
<br/>
<br/>
/api/v1.0/precipitation<br/>
Convert the query results to a dictionary using date as the key and prcp as the value.<br/>
Return the JSON representation of your dictionary.<br/>
<br/>
<br/>
/api/v1.0/stations<br/>
Return a JSON list of stations from the dataset.<br/>
<br/>
<br/>
/api/v1.0/tobs<br/>
Query the dates and temperature observations of the most active station for the last year of data.<br/>
Return a JSON list of temperature observations (TOBS) for the previous year.<br/>
<br/>
<br/>
/api/v1.0/[start] and /api/v1.0/[start]/[end]<br/>
Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.<br/>
When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.<br/>
When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.<br/>
"""
    return message

# 2nd route: Precipitation
@app.route("/api/v1.0/precipitation")
def prcp():
    bell = Session(engine)
    data = (
        bell.query(Measurement.date, Measurement.prcp)
        .filter(Measurement.date > "2016-08-22")
        .all()
    )
    result = {}
    for d, p in data:
        result[d] = p
    result_json = json.dumps(result, indent=4)
    return result_json

# 3rd route: Station
@app.route("/api/v1.0/stations")
def prcp():
    bell = Session(engine)
    data = bell.query(Measurement.station,func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    result = []
    for stat, cnt in data:
        result.append(stat)
    station_names = {}
    station_names["Stations"] = result
    result_json = json.dumps(result, indent=4)
    return result_json

# 4th route TOBS
@app.route("/api/v1.0/tobs")
def tobs():
    bell = Session(engine)
    Station_top = "USC00519281"
    data = bell.query(Measurement.date,Measurement.tobs).filter(Measurement.date>'2016-08-22').filter(Measurement.station == Station_top).all()

    result_json = json.dumps(data)
    return result_json

# 5th route: start date
@app.route("/api/v1.0/<start>")
def start_func(start):
    end_date = "2017-08-23"
    bell = Session(engine)
    data = (
        bell.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs),func.count(Measurement.tobs) ).filter(Measurement.date >= start).all()
    )
   
    result_json = json.dumps(data)
    return result_json


# 6th route: stare and end date
@app.route("/api/v1.0/<start>/<end>")
def end_func(start, end):   
    bell = Session(engine)
    data = (
        bell.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs),func.count(Measurement.tobs) ).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    )
    bell.close()
    result_json = json.dumps(data)
    return result_json



if __name__ == '__main__':
    app.run(debug =  True)

    

        
