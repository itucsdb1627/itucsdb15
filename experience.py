import datetime
from flask import redirect
from flask import request
from flask import flash
from flask import url_for
import psycopg2 as dbapi2
from flask import render_template
from config import app


@app.route('/experience/db')
def init_experience_database():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    cursor.execute('''
    DROP TABLE IF EXISTS EXPERIENCE CASCADE;
    ''')
    query = """CREATE TABLE IF NOT EXISTS EXPERIENCE (
    ID SERIAL PRIMARY KEY,
    COMPANYNAME VARCHAR(90),
    YEARSTART VARCHAR(30) NULL,
    YEAREND VARCHAR(30) NULL,
    POSITION VARCHAR(30) NULL,
    PERSONID INTEGER,
    FOREIGN KEY (PERSONID)
    REFERENCES MAINDATA (ID)
    ON DELETE CASCADE)"""
    cursor.execute(query)
    connection.commit()
    return redirect(url_for('home_page'))

def showexperience_page(personid):
        connection = dbapi2.connect(app.config['dsn'])
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM EXPERIENCE WHERE PERSONID = %s """,[personid])
        connection.commit()
        experience = [(key, CompanyName,YearStart,YearEnd,Position,Personid )
                        for key, CompanyName,YearStart,YearEnd,Position,Personid  in cursor]
        return experience


def addexperience_page(personid):    
        CompanyName = request.form['CompanyName']
        YearStart = request.form['YearStart']
        YearEnd = request.form['YearEnd']
        Position = request.form['Position']
        connection = dbapi2.connect(app.config['dsn'])
        cursor = connection.cursor()
        cursor.execute("""
        INSERT INTO EXPERIENCE (COMPANYNAME, YEARSTART,YEAREND,POSITION,PERSONID)
        VALUES (%s, %s, %s,%s, %s) """,
        (CompanyName, YearStart,YearEnd,Position,personid ))
        connection.commit() 

def deleteexperience_page(personid):         
            id = request.form['id']
            connection = dbapi2.connect(app.config['dsn'])
            cursor = connection.cursor()
            cursor.execute( """ DELETE FROM EXPERIENCE WHERE ID =%s """,[id])
            connection.commit()  
            
def updateexperience_page(personid): 
            experience = request.form['id']
            return experience 
            
def searchexperience_page(personid): 
            CompanyName = request.form['CompanyName']
            connection = dbapi2.connect(app.config['dsn'])
            cursor = connection.cursor()
            cursor.execute( "SELECT * FROM EXPERIENCE WHERE COMPANYNAME LIKE %s",(CompanyName,))
            connection.commit() 
            experience = [(key, CompanyName,YearStart,YearEnd,Position,personid )
                        for key, CompanyName, YearStart,YearEnd,Position,personid  in cursor]
            return experience

def show_experience_update_value(experienceid): 
            connection = dbapi2.connect(app.config['dsn'])
            cursor = connection.cursor()
            cursor.execute( "SELECT * FROM EXPERIENCE WHERE ID=%s",(experienceid,))
            connection.commit() 
            UpdateExperienceValue = [(key, CompanyName,YearStart,YearEnd,Position,personid )
                        for key, CompanyName, YearStart,YearEnd,Position,personid  in cursor]
            return UpdateExperienceValue
      
@app.route('/profil/editexperience/<experienceid>,<personid>', methods=['GET', 'POST'])
def edit_experience(experienceid,personid):
    if request.method == 'GET': 
        return render_template('experience_edit.html')
    else:
         if 'UpdateExperience' in request.form:
             SchoolName = request.form['CompanyName']
             YearStart = request.form['YearStart']
             YearEnd = request.form['YearEnd']
             Position = request.form['Position']
             connection = dbapi2.connect(app.config['dsn'])
             cursor = connection.cursor()
             cursor.execute(""" UPDATE EXPERIENCE SET COMPANYNAME = %s, YEARSTART= %s,YEAREND= %s,POSITION= %s WHERE ID = %s """,
             (SchoolName, YearStart,YearEnd,Position, experienceid))
             connection.commit()   
             return redirect(url_for('profil_page',personid=personid))

@app.route('/experience/deletedb')
def  deleteexperience_db():
     connection = dbapi2.connect(app.config['dsn'])
     cursor = connection.cursor()
     cursor.execute("""DROP TABLE EXPERIENCE""" )
     connection.commit()
     return render_template('profil.html')  