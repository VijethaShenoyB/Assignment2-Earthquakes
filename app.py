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
  cursor.execute("select time, latitude, longitude, mag,id, place from equake where mag >"+getmag+";")
  rows = cursor.fetchall()
  cursor.execute("select count(*) as Num_of_Earthquakes from equake where mag > "+getmag+";")
  count = cursor.fetchall()
  return render_template('display.html', ecount=count[0][0], setquakes=rows)

@app.route("/rangeDisplay" , methods=['GET','POST'])
def rangeMag():
  getmagRange1 = str(request.args.get('fmagnRange1'))
  getmagRange2 = str(request.args.get('fmagnRange2'))
  getdateRange1 = str(request.args.get('fdateRange1'))
  getdateRange2 = str(request.args.get('fdateRange2'))
  cursor.execute("select time, latitude, longitude, mag,id, place from equake where mag >= "+getmagRange1+" and mag <= "+getmagRange2+" AND time between '"+getdateRange1+"' and '"+getdateRange2+"';")
  rangeRows = cursor.fetchall()
  return render_template('rangeDisplay.html', setrangeRows=rangeRows)

if __name__ == '__main__':
	app.run()

