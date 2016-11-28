import datetime
from flask import redirect
from flask import request
from flask import flash
from flask import url_for
import psycopg2 as dbapi2
from flask import render_template
from config import app


@app.route('/profilpicture/db')
def init_profilpicture_database():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    cursor.execute('''
    DROP TABLE IF EXISTS PROFILPICTURE CASCADE;
    ''')
    query = """CREATE TABLE IF NOT EXISTS PROFILPICTURE (
    ID SERIAL PRIMARY KEY,
    PROFILURL VARCHAR(90),
    PERSONID INTEGER,
    FOREIGN KEY (PERSONID)
    REFERENCES MAINDATA (ID)
    ON DELETE CASCADE)"""
    cursor.execute(query)
    connection.commit()
    return redirect(url_for('home_page'))

def showprofilpicture(personid):
        connection = dbapi2.connect(app.config['dsn'])
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM PROFILPICTURE WHERE PERSONID = %s """,[personid])
        pic= cursor.fetchone()
        connection.commit()
        picture=pic[1]
        return picture



def addprofilpicture(personid):    
        ProfilPicture = request.form['ProfilPicture']
        connection = dbapi2.connect(app.config['dsn'])
        cursor = connection.cursor()
        cursor.execute("""
        INSERT INTO PROFILPICTURE (PROFILURL,PERSONID)
        VALUES (%s, %s) """,
        (ProfilPicture,personid ))
        connection.commit() 

@app.route('/profilpictureedit/<personid>')
def profilpictureedit_page(personid):
    return render_template('profil_information_edit.html',personid=personid) 
    

@app.route('/profilpicture/deletedb')
def  deleteprofilpicture_db():
     connection = dbapi2.connect(app.config['dsn'])
     cursor = connection.cursor()
     cursor.execute("""DROP TABLE PROFILPICTURE""" )
     connection.commit()
     return render_template('profil.html') 