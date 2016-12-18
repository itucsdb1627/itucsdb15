import datetime
from flask import redirect
from flask import request
from flask import flash
from flask import url_for
import psycopg2 as dbapi2
from flask import render_template
from config import app


@app.route('/publishes/init')
def init_publishes_database():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    cursor.execute('''
    DROP TABLE IF EXISTS PUBLISHES CASCADE;
    ''')
    query = """CREATE TABLE IF NOT EXISTS PUBLISHES (
    ID SERIAL PRIMARY KEY,
    ESSAYTYPE VARCHAR(90) NOT NULL,
    PUBLISHNAME VARCHAR(90) NOT NULL,
    PUBLISHCONTENT VARCHAR(500) NOT NULL,
    PUBLISHDATE DATE NOT NULL,
    PERSONID INTEGER,
    FOREIGN KEY (PERSONID)
    REFERENCES MAINDATA (ID)
    ON DELETE CASCADE)"""
    cursor.execute(query)
    connection.commit()
    return redirect(url_for('home_page'))

def expresspublishes_page(personid):
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM PUBLISHES WHERE PERSONID = %s """,[personid])
    connection.commit()
    publishes = [(key, EssayType,PublishName,PublishContent,PublishDate,personid)
                        for key, EssayType,PublishName,PublishContent,PublishDate,personid in cursor]
    return publishes

def addpublishes_page(personid):
    EssayType = request.form['EssayType']
    PublishName=request.form['PublishName']
    PublishContent = request.form['PublishContent']
    PublishDate = request.form['PublishDate']
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO PUBLISHES (ESSAYTYPE,PUBLISHNAME,PUBLISHCONTENT,PUBLISHDATE,PERSONID)
    VALUES (%s, %s, %s, %s,%s) """,
    (EssayType,PublishName,PublishContent,PublishDate,personid))
    connection.commit()

def deletepublishes_page(personid):
    id = request.form['id']
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    cursor.execute( """ DELETE FROM PUBLISHES WHERE ID =%s """,[id])
    connection.commit()

def updatepublishes_page(personid):
    publishes = request.form['id']
    return publishes

def searchpublishes_page(personid):
    PublishName = request.form['PublishName']
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    cursor.execute( "SELECT * FROM PUBLISHES WHERE PUBLISHNAME LIKE %s",(PublishName,))
    connection.commit()
    publishes = [(key, EssayType,PublishName,PublishContent,PublishDate,personid)
            for key, EssayType,PublishName,PublishContent,PublishDate,personid in cursor]
    return publishes


@app.route('/ilgialanlari/updatepublishes/<publishesid>,<personid>', methods=['GET', 'POST'])
def update_publishes(publishesid,personid):
    if request.method == 'GET':
        return render_template('updatepublishes.html')
    else:
         if 'Updatepublishes' in request.form:
             EssayType = request.form['EssayType']
             PublishName=request.form['PublishName']
             PublishContent = request.form['PublishContent']
             PublishDate = request.form['PublishDate']
             connection = dbapi2.connect(app.config['dsn'])
             cursor = connection.cursor()
             cursor.execute(""" UPDATE PUBLISHES SET ESSAYTYPE = %s, PUBLISHNAME= %s, PUBLISHCONTENT= %s, PUBLISHDATE= %s WHERE ID = %s """,
             (EssayType,PublishName,PublishContent,PublishDate, publishesid))
             connection.commit()
             return redirect(url_for('ilgialanlari_page',personid=personid))

@app.route('/ilgialanlari/deletepublishes')
def delete_publishes():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    cursor.execute("""DROP TABLE PUBLISHES""" )
    connection.commit()
    return render_template('ilgialanlari.html')

