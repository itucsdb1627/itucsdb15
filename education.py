import datetime
from flask import redirect
from flask import request
from flask import flash
from flask import url_for
import psycopg2 as dbapi2
from flask import render_template
from config import app



@app.route('/education/db')
def init_education_database():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    cursor.execute('''
    DROP TABLE IF EXISTS KISILER CASCADE;
    ''')
    query = """CREATE TABLE IF NOT EXISTS EDUCATION (
    ID SERIAL PRIMARY KEY,
    SCHOOLNAME VARCHAR(90),
    YEARSTART VARCHAR(30) NULL,
    YEAREND VARCHAR(30) NULL,
    PERSONID INTEGER,
    GPA VARCHAR(30) NULL,
    FOREIGN KEY (PERSONID)
    REFERENCES MAINDATA (ID)
    ON DELETE CASCADE)"""
    cursor.execute(query)
    connection.commit()
    return redirect(url_for('home_page'))






def showeducation_page(personid):
        connection = dbapi2.connect(app.config['dsn'])
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM EDUCATION WHERE PERSONID = %s """,[personid])
        connection.commit()
        education = [(key, SchoolName,YearStart,YearEnd,Personid ,Gpa)
                        for key, SchoolName, YearStart, YearEnd, Personid ,Gpa in cursor]
        return education
    
    
def addeducation_page(personid):    
        SchoolName = request.form['SchoolName']
        YearStart = request.form['YearStart']
        YearEnd = request.form['YearEnd']
        Gpa = request.form['Gpa']
        connection = dbapi2.connect(app.config['dsn'])
        cursor = connection.cursor()
        cursor.execute("""
        INSERT INTO EDUCATION (SCHOOLNAME, YEARSTART,YEAREND,PERSONID,GPA)
        VALUES (%s, %s, %s, %s, %s) """,
        (SchoolName, YearStart,YearEnd,personid ,Gpa))
        connection.commit()   

        
def deleteeducation_page(personid):         
            id = request.form['id']
            connection = dbapi2.connect(app.config['dsn'])
            cursor = connection.cursor()
            cursor.execute( """ DELETE FROM EDUCATION WHERE ID =%s """,[id])
            connection.commit()   
        
def updateeducation_page(personid): 
            educationid = request.form['id']
            return educationid

def searcheducation_page(personid): 
            SchoolName = request.form['SchoolName']
            connection = dbapi2.connect(app.config['dsn'])
            cursor = connection.cursor()
            cursor.execute( "SELECT * FROM EDUCATION WHERE SCHOOLNAME LIKE %s",(SchoolName,))
            connection.commit() 
            education = [(key, SchoolName,YearStart,YearEnd,personid ,Gpa)
                        for key, SchoolName, YearStart,YearEnd,personid , Gpa in cursor]
            return education
        
def show_education_update_value(educationid): 
            connection = dbapi2.connect(app.config['dsn'])
            cursor = connection.cursor()
            cursor.execute( "SELECT * FROM EDUCATION WHERE ID=%s",(educationid,))
            connection.commit() 
            UpdateEducationValue = [(key, SchoolName,YearStart,YearEnd,personid ,Gpa)
                        for key, SchoolName, YearStart,YearEnd,personid , Gpa in cursor]
            return UpdateEducationValue


       
@app.route('/profil/editeducation/<educationid>,<personid>', methods=['GET', 'POST'])
def edit_education(educationid,personid):
    if request.method == 'GET': 
        return render_template('education_edit.html')
    else:
         if 'Update' in request.form:
             SchoolName = request.form['SchoolName']
             YearStart = request.form['YearStart']
             YearEnd = request.form['YearEnd']
             Gpa = request.form['Gpa']
             connection = dbapi2.connect(app.config['dsn'])
             cursor = connection.cursor()
             cursor.execute(""" UPDATE EDUCATION SET SCHOOLNAME = %s, YEARSTART= %s,YEAREND= %s, GPA= %s WHERE ID = %s """,
             (SchoolName, YearStart,YearEnd, Gpa, educationid))
             connection.commit()   
             return redirect(url_for('profil_page',personid=personid))
             
@app.route('/education/deletedb')
def  deleteeducation_db():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    cursor.execute("""DROP TABLE EDUCATION""" )
    connection.commit()
    return render_template('profil.html')  