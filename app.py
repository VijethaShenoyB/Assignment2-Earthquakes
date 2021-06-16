from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import csv
import numpy as np
import os
import pyodbc
import sys
import redis
from time import time
import hashlib
import pickle
app = Flask(__name__)

server = 'shenoyserver.database.windows.net'
database = 'ShenoyDB'
username = 'vijethashenoy'
password = 'Vijushenoy96'
driver= '{ODBC Driver 17 for SQL Server}'

cnxn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
cursor = cnxn.cursor()

@app.route('/', methods=["POST","GET"])
def hello():
	return render_template('index.html')

@app.route("/display" , methods=['GET','POST'])
def greaterMag():
  getmag = str(request.args.get('fmagnitude'))
  cursor.execute("select etime, ptime, latitude, longitude, mag,id, place from quake where mag >"+getmag+";")
  rows = cursor.fetchall()
  cursor.execute("select count(*) as Num_of_Earthquakes from quake where mag > "+getmag+";")
  count = cursor.fetchall()
  return render_template('display.html', ecount=count[0][0], setquakes=rows)

@app.route("/rangeDisplay" , methods=['GET','POST'])
def rangeMag():
  getmagRange1 = str(request.args.get('fmagnRange1'))
  getmagRange2 = str(request.args.get('fmagnRange2'))
  getdateRange1 = str(request.args.get('fdateRange1'))
  getdateRange2 = str(request.args.get('fdateRange2'))
  cursor.execute("select etime, ptime, latitude, longitude, mag, id, place from quake where mag >= "+getmagRange1+" and mag <= "+getmagRange2+" AND time between '"+getdateRange1+"' and '"+getdateRange2+"';")
  rangeRows = cursor.fetchall()
  return render_template('rangeDisplay.html', setrangeRows=rangeRows)


@app.route("/etimeDisplay" , methods=['GET','POST'])
def rangeMag():
  getetimeRange1 = str(request.args.get('fetimeRange1'))
  getetimeRange2 = str(request.args.get('fetimeRange2'))
  getdepthRange1 = str(request.args.get('fdepthRange1'))
  getdepthRange2 = str(request.args.get('fdepthRange2'))
  cursor.execute("select etime, ptime, latitude, longitude, mag, id, place from quake where etime >= "+getetimeRange1+" and etime <= "+getetimeRange2+" AND depth between '"+getdepthRange1+"' and '"+getdepthRange2+"';")
  eTimerangeRows = cursor.fetchall()
  cursor.execute("select count(*) as Num_of_Earthquakes from quake where depth >= "+getetimeRange1+" and mag <= "+getetimeRange2+" AND depth between '"+getdepthRange1+"' and '"+getdepthRange2+"';")
  depthcount = cursor.fetchall()
  return render_template('etimeDisplay.html', setdepthcount=depthcount[0][0],seteTimerangeRows=eTimerangeRows)


@app.route("/timeDisplay" , methods=['GET','POST'])
def timeMag():
  gettimeRange1 = str(request.args.get('ftimeRange1'))
  gettimeRange2 = str(request.args.get('ftimeRange2'))
  cursor.execute("select max(mag), latitude, longitude, id, place from quake where (time>="+gettimeRange1+" and time<= "+gettimeRange2+");")
  timeRows = cursor.fetchall()
  return render_template('timeDisplay.html',settimeRows=timeRows)


@app.route("/locationDisplay" , methods=['GET','POST'])
def location():
  getlongitude = str(request.args.get('flongitude'))
  getlatitude = str(request.args.get('flatitude'))
  getkmrange = str(request.args.get('fkmrange'))

  leftlat = float(getlatitude)-float(getkmrange)/111   #converting km to degree
  rightlat = float(getlatitude)+float(getkmrange)/111
  uplong =   float(getlongitude)+float(getkmrange)/111
  downlong = float(getlongitude)-float(getkmrange)/111

  cursor.execute("select time, latitude, longitude, mag,id, place from quake;")
  locationRows = cursor.fetchall()
  return render_template('locationDisplay.html', setlocationRows=locationRows)


@app.route("/clusterDisplay" , methods=['GET','POST'])
def cluster():
    getclustermag = str(request.args.get('fclustermag'))
    cursor.execute("select time, latitude, longitude, mag,id, place from quake where mag = "+getclustermag+";")
    clusterrows = cursor.fetchall()
    cursor.execute("select count(*) as Num_of_Earthquakes from quake where mag = "+getclustermag+";")
    clustercount = cursor.fetchall()
    return render_template('clusterDisplay.html', setclustercount=clustercount[0][0], setclusterquakes=clusterrows)

@app.route("/nightDisplay" , methods=['GET','POST'])
def nightdisplay():
  getlargemag = str(request.args.get('flargemag'))
  cursor.execute("select time, latitude, longitude, mag,id, place from quake where mag> "+getlargemag+" and  (DATEADD(day, -DATEDIFF(day, 0, time), time) > '00:10:10.000' and DATEADD(day, -DATEDIFF(day, 0, time), time) < '05:00:00.000');")
  nightRows = cursor.fetchall()
  cursor.execute("select count(*) from quake where mag> "+getlargemag+" and  (DATEADD(day, -DATEDIFF(day, 0, time), time) > '00:10:10.000' and DATEADD(day, -DATEDIFF(day, 0, time), time) < '05:00:00.000');")
  nightcount = cursor.fetchall()
  return render_template('nightDisplay.html', setnightcount=nightcount[0][0],setnightRows=nightRows)




if __name__ == '__main__':
	app.run()

