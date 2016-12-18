import datetime
from flask import redirect
from flask import request
from flask import flash
from flask import url_for
import psycopg2 as dbapi2
from flask import render_template
from config import app


@app.route('/ilgialanlari/init')
def init_groups_database():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    cursor.execute('''
    DROP TABLE IF EXISTS GRUP CASCADE;
    ''')
    query = """CREATE TABLE IF NOT EXISTS GRUP (
    ID SERIAL PRIMARY KEY,
    GROUPNAME VARCHAR(90) NOT NULL,
    EXPLANATION VARCHAR(400) NOT NULL,
    STARTDATE DATE NOT NULL,
    SECTOR VARCHAR(90) NOT NULL,
    PERSONID INTEGER,
    FOREIGN KEY (PERSONID)
    REFERENCES MAINDATA (ID)
    ON DELETE CASCADE)"""
    cursor.execute(query)
    connection.commit()
    return redirect(url_for('home_page'))

def expressgrup_page(personid):
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM GRUP WHERE PERSONID = %s """,[personid])
    connection.commit()
    grup = [(key, GroupName,Explanation,StartDate,Sector,personid)
                        for key, GroupName, Explanation,StartDate ,Sector, personid in cursor]
    return grup

def addgrup_page(personid):
    GroupName = request.form['GroupName']
    Explanation = request.form['Explanation']
    StartDate = request.form['StartDate']
    Sector = request.form['Sector']
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO GRUP (GROUPNAME, EXPLANATION,STARTDATE,SECTOR,PERSONID)
    VALUES (%s, %s, %s, %s, %s) """,
    (GroupName, Explanation,StartDate,Sector,personid))
    connection.commit()

def deletegrup_page(personid):
    id = request.form['id']
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    cursor.execute( """ DELETE FROM GRUP WHERE ID =%s """,[id])
    connection.commit()

def updategrup_page(personid):
    grupid = request.form['id']
    return grupid

def searchgrup_page(personid):
    GroupName = request.form['GroupName']
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    cursor.execute( "SELECT * FROM GRUP WHERE GROUPNAME LIKE %s",(GroupName,))
    connection.commit()
    grup = [(key, GroupName,Explanation, StartDate, Sector,personid)
            for key, GroupName, Explanation, StartDate, Sector,personid in cursor]
    return grup


@app.route('/ilgialanlari/updategroups/<grupid>,<personid>', methods=['GET', 'POST'])
def update_groups(grupid,personid):
    if request.method == 'GET':
        return render_template('updategroups.html')
    else:
         if 'Update' in request.form:
             GroupName = request.form['GroupName']
             Explanation = request.form['Explanation']
             StartDate = request.form['StartDate']
             Sector = request.form['Sector']
             connection = dbapi2.connect(app.config['dsn'])
             cursor = connection.cursor()
             cursor.execute(""" UPDATE GRUP SET GROUPNAME = %s, EXPLANATION= %s, STARTDATE= %s, SECTOR= %s WHERE ID = %s """,
             (GroupName, Explanation, StartDate, Sector, grupid))
             connection.commit()
             return redirect(url_for('ilgialanlari_page',personid=personid))

@app.route('/ilgialanlari/deletegroups')
def delete_groups():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    cursor.execute("""DROP TABLE GRUP""" )
    connection.commit()
    return render_template('ilgialanlari.html')

