import json
import datetime
import re
import os
import psycopg2 as dbapi2

from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
from flask.helpers import url_for



from flask.globals import request
from pip.utils import backup_dir

app = Flask(__name__)

from profil import *
from maindatadb import *
from ilgialanlari import *



def get_elephantsql_dsn(vcap_services):
    """Returns the data source name for ElephantSQL."""
    parsed = json.loads(vcap_services)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
    user, password, host, _, port, dbname = match.groups()
    dsn = """user='{}' password='{}' host='{}' port={}
             dbname='{}'""".format(user, password, host, port, dbname)
    return dsn

@app.route('/',methods = ['GET','POST'])
def signin_page():
    if request.method=='POST':
        now = datetime.datetime.now()
        email = request.form['email']
        password = request.form['password']
        connection = dbapi2.connect(app.config['dsn'])
        cursor = connection.cursor()
        cursor.execute("SELECT ID FROM MAINDATA WHERE EMAIL=%s AND  PASSWORD=%s",(email,password))
        idd= cursor.fetchone()
        personid=idd[0]
        return render_template('home.html', personid = personid)
    elif request.method == 'GET':
        return render_template('signin.html')



@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/initdb')
def initialize_database():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """DROP TABLE IF EXISTS COUNTER"""
        cursor.execute(query)

        query = """CREATE TABLE COUNTER (N INTEGER)"""
        cursor.execute(query)

        query = """INSERT INTO COUNTER (N) VALUES (0)"""
        cursor.execute(query)

        connection.commit()
    return redirect(url_for('home_page'))
@app.route('/count')
def counter_page():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = "UPDATE COUNTER SET N = N + 1"
        cursor.execute(query)
        connection.commit()

        query = "SELECT N FROM COUNTER"
        cursor.execute(query)
        count = cursor.fetchone()[0]
    return "This page was accessed %d times." % count



        
@app.route('/baglantilar')
def baglantilar_page():
    return render_template('baglantilar.html')
@app.route('/hakkimizda')
def hakkimizda_page():
    return render_template('hakkimizda.html')
@app.route('/isfirsatlari')
def isfirsatlari_page():
    return render_template('isfirsatlari.html')


@app.route('/signup',methods=['POST','GET'])
def signup_page():

     if request.method=='POST':
      mssg=request.form['email']
      psswrd=request.form['password']
      name=request.form['name']
      surname=request.form['surname']
      with dbapi2.connect(app.config['dsn']) as connection:
       cursor = connection.cursor()
      query= """ INSERT INTO MAINDATA(EMAIL,PASSWORD,NAME,SURNAME) VALUES ('%s','%s','%s','%s')"""  % (mssg,psswrd,name,surname)
      cursor.execute(query)
      connection.commit()
     return render_template('signup.html')    
    


@app.route('/baglantilar/initdb')
def initialize_database_baglantilar():
    connection=dbapi2.connect(app.config['dsn'])
    cursor=connection.cursor()

    query=""" DROP TABLE IF EXISTS BAGLANTILAR CASCADE"""
    cursor.execute(query)
    query="""CREATE TABLE BAGLANTILAR(ID SERIAL PRIMARY KEY, FIRSTNAME VARCHAR(50) NOT NULL,SURNAME VARCHAR(50) NOT NULL,COMPANYNAME VARCHAR(50),MUTUALCONNECTIONNUMBER INTEGER,TOTALCONNECTIONNUMBER INTEGER)"""
    cursor.execute(query)
    query="""INSERT INTO BAGLANTILAR(FIRSTNAME,SURNAME,COMPANYNAME,MUTUALCONNECTIONNUMBER,TOTALCONNECTIONNUMBER) VALUES('BURAK','SIMSEK','ITU','10','40')"""
    cursor.execute(query)
    connection.commit()
    return redirect(url_for('baglantilar_page'))





@app.route('/hakkimizda/activedb')
def initialize_database_hakkimizda():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()

    query = """DROP TABLE IF EXISTS HAKKIMIZDA CASCADE"""
    cursor.execute(query)
    query = """CREATE TABLE HAKKIMIZDA(ID SERIAL PRIMARY KEY, CONTENT VARCHAR(200) NOT NULL , MESSAGE VARCHAR(100) NOT NULL)"""
    cursor.execute(query)
    query = """INSERT INTO HAKKIMIZDA(CONTENT, MESSAGE) VALUES('Jobs for you. The use of the professional business world, welcome to the communication network' , 'Your dreams will come true.')"""
    cursor.execute(query)
    connection.commit()
    return redirect(url_for('hakkimizda_page'))

@app.route('/isfirsatlari/starteddb')
def initialize_database_isfirsatlari():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = coDnnection.cursor()

    query = """DROP TABLE IF EXISTS ISFIRSATLARI CASCADE"""
    cursor.execute(query)
    query = """CREATE TABLE ISFIRSATLARI (ID SERIAL PRIMARY KEY, FNAME VARCHAR(20) NOT NULL , LNAME VARCHAR(50) NOT NULL , IL VARCHAR(20) NOT NULL, SEKTOR VARCHAR(50) NOT NULL)"""
    cursor.execute(query)
    query = """INSERT INTO ISFIRSATLARI (FNAME, LNAME, IL, SEKTOR) VALUES ('ERDEM','SAHIN', 'ISTANBUL', 'YAZILIM')"""
    cursor.execute(query)
    connection.commit()
    return redirect(url_for('isfirsatlari_page'))

if __name__ == '__main__':
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5001, True

    VCAP_SERVICES = os.getenv('VCAP_SERVICES')
    if VCAP_SERVICES is not None:
        app.config['dsn'] = get_elephantsql_dsn(VCAP_SERVICES)
    else:
        app.config['dsn'] = """user='vagrant' password='vagrant'
                               host='localhost' port=1234 dbname='itucsdb'"""

    app.run(host='0.0.0.0', port=port, debug=debug)
