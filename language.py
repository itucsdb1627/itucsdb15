import datetime
from flask import redirect
from flask import request
from flask import flash
from flask import url_for
import psycopg2 as dbapi2
from flask import render_template
from config import app


@app.route('/language/db')
def init_language_database():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    cursor.execute('''
    DROP TABLE IF EXISTS LANGUAGE CASCADE;
    ''')
    query = """CREATE TABLE IF NOT EXISTS LANGUAGE (
    ID SERIAL PRIMARY KEY,
    LANGUAGENAME VARCHAR(90),
    LEVEL VARCHAR(30) NULL,
    PERSONID INTEGER,
    FOREIGN KEY (PERSONID)
    REFERENCES MAINDATA (ID)
    ON DELETE CASCADE)"""
    cursor.execute(query)
    connection.commit()
    return redirect(url_for('home_page'))

def showlanguage(personid):
        connection = dbapi2.connect(app.config['dsn'])
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM LANGUAGE WHERE PERSONID = %s """,[personid])
        connection.commit()
        language = [(key, LanguageName,Level,Personid )
                        for key, LanguageName, Level,Personid  in cursor]
        return language

def deletelanguage(personid):         
            id = request.form['id']
            connection = dbapi2.connect(app.config['dsn'])
            cursor = connection.cursor()
            cursor.execute( """ DELETE FROM LANGUAGE WHERE ID =%s """,[id])
            connection.commit() 
            
def updatelanguage(personid): 
            language = request.form['id']
            return language 

def addlanguage(personid):    
        LanguageName = request.form['LanguageName']
        Level = request.form['Level']
        connection = dbapi2.connect(app.config['dsn'])
        cursor = connection.cursor()
        cursor.execute("""
        INSERT INTO LANGUAGE (LANGUAGENAME, LEVEL,PERSONID)
        VALUES (%s, %s, %s) """,
        (LanguageName, Level,personid ))
        connection.commit() 

@app.route('/profil/editlanguage/<languageid>,<personid>', methods=['GET', 'POST'])
def edit_language(languageid,personid):
    if request.method == 'GET': 
        return render_template('language_edit.html')
    else:
         if 'UpdateLanguage' in request.form:
             LanguageName = request.form['LanguageName']
             Level = request.form['Level']
             connection = dbapi2.connect(app.config['dsn'])
             cursor = connection.cursor()
             cursor.execute(""" UPDATE LANGUAGE SET LANGUAGENAME = %s, LEVEL= %s WHERE ID = %s """,
             (LanguageName, Level, languageid))
             connection.commit()   
             return redirect(url_for('profil_page',personid=personid))

def searchlanguage(personid): 
            LanguageName = request.form['LanguageName']
            connection = dbapi2.connect(app.config['dsn'])
            cursor = connection.cursor()
            cursor.execute( "SELECT * FROM LANGUAGE WHERE LANGUAGENAME LIKE %s",(LanguageName,))
            connection.commit() 
            language = [(key, LanguageName,Level,personid )
                        for key, LanguageName, Level,personid  in cursor]
            return language


@app.route('/language/deletedb')
def  deletelanguage_db():
     connection = dbapi2.connect(app.config['dsn'])
     cursor = connection.cursor()
     cursor.execute("""DROP TABLE LANGUAGE""" )
     connection.commit()
     return render_template('profil.html')  