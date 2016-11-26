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

app = Flask(__name__)

class Education:
    def __init__(self, SchoolName, Year, Gpa):
        self.SchoolName = SchoolName
        self.Year = Year
        self.Gpa = Gpa
       

@app.route('/profil/db')
def init_education_database():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    cursor.execute('''
    DROP TABLE IF EXISTS KISILER CASCADE;
    ''')
    query = """CREATE TABLE IF NOT EXISTS EDUCATION (
    ID SERIAL PRIMARY KEY,
    SCHOOLNAME VARCHAR(90),
    YEAR VARCHAR(30) NULL,
    PERSONID INTEGER REFERENCES MAINDATA (ID),
    GPA VARCHAR(30) NULL)"""
    cursor.execute(query)
    connection.commit()
    return redirect(url_for('home_page'))
     

def add_education(self, education):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO EDUCATION (SCHOOLNAME, YEAR, GPA)
                    VALUES (%s, %s, %s) """,
                    (education.SchoolName, education.Year, education.Gpa))
                connection.commit()   
    

@app.route('/profil/<personid>', methods=['GET', 'POST'])
def profil_page(personid):
    if request.method == 'GET':
        connection = dbapi2.connect(app.config['dsn'])
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM EDUCATION WHERE PERSONID = %s """,[personid])
        connection.commit()
        education = [(key, SchoolName,Year,Personid ,Gpa)
                        for key, SchoolName, Year,Personid ,Gpa in cursor]
        return render_template('profil.html', education = education,personid=personid)
        
        
    else:
        if 'Add' in request.form:
            SchoolName = request.form['SchoolName']
            Year = request.form['Year']
            Gpa = request.form['Gpa']
            connection = dbapi2.connect(app.config['dsn'])
            cursor = connection.cursor()
            cursor.execute("""
            INSERT INTO EDUCATION (SCHOOLNAME, YEAR,PERSONID,GPA)
            VALUES (%s, %s, %s, %s) """,
            (SchoolName, Year,personid ,Gpa))
            connection.commit()   
            return redirect(url_for('profil_page',personid=personid))
        
        elif 'Delete' in request.form:
            id = request.form['id']
            connection = dbapi2.connect(app.config['dsn'])
            cursor = connection.cursor()
            cursor.execute( """ DELETE FROM EDUCATION WHERE ID =%s """,[id])
            connection.commit()   
            return redirect(url_for('profil_page'))
        elif 'Update' in request.form:
            educationid = request.form['id']
            return render_template('education_edit.html', key = educationid)
        elif 'Search' in request.form:
            SchoolName = request.form['SchoolName']
            connection = dbapi2.connect(app.config['dsn'])
            cursor = connection.cursor()
            cursor.execute( "SELECT * FROM EDUCATION WHERE SCHOOLNAME LIKE %s",(SchoolName,))
            connection.commit() 
            education = [(key, SchoolName,Year, Gpa)
                        for key, SchoolName, Year, Gpa in cursor]
            return render_template('profil.html',education = education)   
        
        
@app.route('/profil/editeducation/<educationid>', methods=['GET', 'POST'])
def edit_education(educationid):
    if request.method == 'GET': 
        return render_template('education_edit.html')
    else:
         if 'Update' in request.form:
             SchoolName = request.form['SchoolName']
             Year = request.form['Year']
             Gpa = request.form['Gpa']
             connection = dbapi2.connect(app.config['dsn'])
             cursor = connection.cursor()
             cursor.execute(""" UPDATE EDUCATION SET SCHOOLNAME = %s, YEAR= %s, GPA= %s WHERE ID = %s """,
             (SchoolName, Year, Gpa, educationid))
             connection.commit()   
             return redirect(url_for('profil_page'))
             
@app.route('/profil/deletedb')
def  delete_db():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    cursor.execute("""DROP TABLE EDUCATION""" )
    connection.commit()
    return render_template('profil.html')

