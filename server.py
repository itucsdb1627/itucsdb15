import datetime
import json
import os
import psycopg2 as dbapi2
import re


from flask import Flask
from flask import redirect
from flask import render_template
from flask.helpers import url_for



app = Flask(__name__)

def get_elephantsql_dsn(vcap_services):
    """Returns the data source name for ElephantSQL."""
    parsed = json.loads(vcap_services)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
    user, password, host, _, port, dbname = match.groups()
    dsn = """user='{}' password='{}' host='{}' port={}
             dbname='{}'""".format(user, password, host, port, dbname)
    return dsn




@app.route('/')
def home_page():
    now = datetime.datetime.now()
    return render_template('home.html', current_time=now.ctime())
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

@app.route('/ilgialanlari')
def ilgialanlari_page():
    return render_template('ilgialanlari.html')
@app.route('/kisiler')
def kisiler_page():
    return render_template('kisiler.html')
@app.route('/baglantilar')
def baglantilar_page():
    return render_template('baglantilar.html')
@app.route('/hakkimizda')
def hakkimizda_page():
    return render_template('hakkimizda.html')
@app.route('/isfirsatlari')
def isfirsatlari_page():
    return render_template('isfirsatlari.html')


@app.route('/kisiler/db')
def initialize_database_eklenmemis_kisiler():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()

    query = """DROP TABLE IF EXISTS EKLENMEMISKISILER CASCADE"""
    cursor.execute(query)
    query = """CREATE TABLE EKLENMEMISKISILER (ID SERIAL PRIMARY KEY, PersonName VARCHAR NOT NULL , PersonSurname VARCHAR NOT NULL , Company VARCHAR NOT NULL)"""
    cursor.execute(query)
    query = """INSERT INTO EKLENMEMISKISILER (PersonName, PersonSurname, Company) VALUES ('ANIL','AGCA', 'IBM')"""
    cursor.execute(query)
    query = """INSERT INTO EKLENMEMISKISILER (PersonName, PersonSurname, Company) VALUES ('YUSUF','AKSOY', 'ORACLE')"""
    cursor.execute(query)
    connection.commit()
    return redirect(url_for('kisiler_page'))


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


@app.route('/ilgialanlari/initiatedb')
def initialize_database_ilgialanlari():
    connection=dbapi2.connect(app.config['dsn'])
    cursor=connection.cursor()

    query=""" DROP TABLE IF EXISTS ILGIALANLARI CASCADE"""
    cursor.execute(query)
    query="""CREATE TABLE ILGIALANLARI(ID SERIAL PRIMARY KEY, GROUPNAME VARCHAR(50) NOT NULL,DESCRYPTION VARCHAR(300) NOT NULL)"""
    cursor.execute(query)
    query="""INSERT INTO ILGIALANLARI(GROUPNAME, DESCRYPTION) VALUES('Data Mining','The group is intended for discussions concerning Data Mining.')"""
    cursor.execute(query)
    query="""INSERT INTO ILGIALANLARI(GROUPNAME, DESCRYPTION) VALUES('Android Programming','Join the Android Programming group to network with people interested in Android Programming.')"""
    cursor.execute(query)
    connection.commit()
    return redirect(url_for('ilgialanlari_page'))


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
