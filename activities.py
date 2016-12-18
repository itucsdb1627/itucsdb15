import datetime
from flask import redirect
from flask import request
from flask import flash
from flask import url_for
import psycopg2 as dbapi2
from flask import render_template
from config import app


@app.route('/activities/init')
def init_activities_database():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    cursor.execute('''
    DROP TABLE IF EXISTS ACTIVITIES CASCADE;
    ''')
    query = """CREATE TABLE IF NOT EXISTS ACTIVITIES (
    ID SERIAL PRIMARY KEY,
    ACTIVITYNAME VARCHAR(150) NOT NULL,
    ACTIVITYCONTENT VARCHAR(400) NOT NULL,
    ACTIVITYDATE DATE NOT NULL,
    PERSONID INTEGER,
    FOREIGN KEY (PERSONID)
    REFERENCES MAINDATA (ID)
    ON DELETE CASCADE)"""
    cursor.execute(query)
    connection.commit()
    return redirect(url_for('home_page'))

def expressactivities_page(personid):
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM ACTIVITIES WHERE PERSONID = %s """,[personid])
    connection.commit()
    activities = [(key,ActivityName,ActivityContent,ActivityDate,personid)
                        for key,ActivityName,ActivityContent,ActivityDate,personid in cursor]
    return activities

def addactivities_page(personid):
    ActivityName=request.form['ActivityName']
    ActivityContent = request.form['ActivityContent']
    ActivityDate = request.form['ActivityDate']
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO ACTIVITIES (ACTIVITYNAME,ACTIVITYCONTENT,ACTIVITYDATE,PERSONID)
    VALUES (%s, %s, %s, %s) """,
    (ActivityName,ActivityContent,ActivityDate,personid))
    connection.commit()

def deleteactivities_page(personid):
    id = request.form['id']
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    cursor.execute( """ DELETE FROM ACTIVITIES WHERE ID =%s """,[id])
    connection.commit()

def updateactivities_page(personid):
    activities = request.form['id']
    return activities

def searchactivities_page(personid):
    ActivityName = request.form['ActivityName']
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    cursor.execute( "SELECT * FROM ACTIVITIES WHERE ACTIVITYNAME LIKE %s",(ActivityName,))
    connection.commit()
    activities = [(key, ActivityName,ActivityContent,ActivityDate,personid)
            for key, ActivityName,ActivityContent,ActivityDate,personid in cursor]
    return activities


@app.route('/ilgialanlari/updateactivities/<activitiesid>,<personid>', methods=['GET', 'POST'])
def update_activities(activitiesid,personid):
    if request.method == 'GET':
        return render_template('updateactivities.html')
    else:
         if 'Updateactivities' in request.form:
             ActivityName = request.form['ActivityName']
             ActivityContent = request.form['ActivityContent']
             ActivityDate = request.form['ActivityDate']
             connection = dbapi2.connect(app.config['dsn'])
             cursor = connection.cursor()
             cursor.execute(""" UPDATE ACTIVITIES SET ACTIVITYNAME= %s, ACTIVITYCONTENT= %s, ACTIVITYDATE= %s WHERE ID = %s """,
             (ActivityName,ActivityContent,ActivityDate, activitiesid))
             connection.commit()
             return redirect(url_for('ilgialanlari_page',personid=personid))

@app.route('/ilgialanlari/deleteactivities')
def delete_activities():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    cursor.execute("""DROP TABLE ACTIVITIES""" )
    connection.commit()
    return render_template('ilgialanlari.html')

