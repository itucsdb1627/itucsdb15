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


from profil import *

from flask.globals import request
from pip.utils import backup_dir

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

@app.route('/',methods = ['GET','POST'])
def signin_page():
    if request.method=='POST':
        now = datetime.datetime.now()
        email = request.form['email']
        password = request.form['password']
        connection = dbapi2.connect(app.config['dsn'])
        cursor = connection.cursor()
        cursor.execute("SELECT ID FROM MAINDATA WHERE EMAIL=%s AND  PASSWORD=%s",(email,password))
        personid = cursor.fetchone()
        connection.commit() 
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

@app.route('/ilgialanlari')
def ilgialanlari_page():
    return render_template('ilgialanlari.html')

@app.route('/profil', methods=['GET', 'POST'])
def profil_page():
    if request.method == 'GET':
        connection = dbapi2.connect(app.config['dsn'])
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM EDUCATION ORDER BY SCHOOLNAME , YEAR , GPA""")
        connection.commit()
        education = [(key, SchoolName,Year, Gpa)
                        for key, SchoolName, Year, Gpa in cursor]
        return render_template('profil.html', education = education)
        
        
    else:
        if 'Add' in request.form:
            SchoolName = request.form['SchoolName']
            Year = request.form['Year']
            Gpa = request.form['Gpa']
            connection = dbapi2.connect(app.config['dsn'])
            cursor = connection.cursor()
            cursor.execute("""
            INSERT INTO EDUCATION (SCHOOLNAME, YEAR, GPA)
            VALUES (%s, %s, %s) """,
            (SchoolName, Year, Gpa))
            connection.commit()   
            return redirect(url_for('profil_page'))
        
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
             
             
        
@app.route('/baglantilar')
def baglantilar_page():
    return render_template('baglantilar.html')
@app.route('/hakkimizda')
def hakkimizda_page():
    return render_template('hakkimizda.html')
@app.route('/isfirsatlari')
def isfirsatlari_page():
    return render_template('isfirsatlari.html')


@app.route('/profil/db')
def initialize_database_eklenmemis_kisiler():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    cursor.execute('''
    DROP TABLE IF EXISTS KISILER CASCADE;
    ''')
    init_education_database(cursor)
    
    connection.commit()
    return redirect(url_for('home_page'))
@app.route('/admin/initdb')
def initialize_maindata_db():
    connection=dbapi2.connect(app.config['dsn'])
    cursor=connection.cursor()

    query=""" DROP TABLE IF EXISTS BAGLANTILAR CASCADE"""
    cursor.execute(query)
    query="""CREATE TABLE MAINDATA(ID SERIAL PRIMARY KEY, EMAIL VARCHAR(50) NOT NULL,PASSWORD VARCHAR(50) NOT NULL)"""
    cursor.execute(query)
    query="""INSERT INTO MAINDATA(EMAIL,PASSWORD) VALUES('BURAK','SIMSEK')"""
    cursor.execute(query)
    connection.commit()
    return redirect(url_for('admin_page'))

@app.route('/admin',methods=['GET','POST'])
def admin_page():

        connection = dbapi2.connect(app.config['dsn'])
        cursor = connection.cursor()
        if request.method == 'GET':
          cursor.execute("""SELECT * FROM MAINDATA ORDER BY  EMAIL , PASSWORD""")
          backupmaindata=cursor.fetchall()
          connection.commit()
          maindata = [(key,email,password)
                 for key,email,password in cursor]
        return render_template('admin.html', maindata = backupmaindata)
@app.route('/admin/deleteuser',methods=['POST','GET'])
def delete_user():
        connection = dbapi2.connect(app.config['dsn'])
        cursor = connection.cursor()
        if request.method=='POST':
          eposta=request.form['email']
          cursor.execute("DELETE FROM MAINDATA WHERE EMAIL= %s",(eposta,))

          cursor.execute("SELECT * FROM MAINDATA")
          backupmaindata=cursor.fetchall()
          connection.commit()
          return redirect(url_for('admin_page',maindata=backupmaindata))
        elif request.method == 'GET':
          return redirect(url_for('admin_page',maindata=backupmaindata))
@app.route('/admin/searchuser',methods=['POST','GET'])
def search_user():
    
    if request.method=='POST':
      emailadd=request.form['emailaddress']
      connection = dbapi2.connect(app.config['dsn'])
      cursor = connection.cursor()
      cursor.execute("SELECT * FROM MAINDATA WHERE EMAIL=%s",(emailadd,))
      connection.commit()
      backupmaindata=[(key,email,password)
                      for key,email,password in cursor]
      
      return render_template('updateuser.html',backupmaindata=backupmaindata)
@app.route('/admin/updateuser/<asdid>',methods=['POST','GET'])
def update_user(asdid):
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    if request.method=='POST':
      
       posta=request.form['email']
       psswd=request.form['password']
       cursor.execute("""UPDATE MAINDATA SET EMAIL=%s,PASSWORD=%s  WHERE ID= %s""" ,(posta,psswd,asdid))
       connection.commit()
      
       return redirect(url_for('admin_page'))
    elif request.method=='GET':
        return render_template('updateuser.html')
@app.route('/signup',methods=['POST','GET'])
def signup_page():

     if request.method=='POST':
      mssg=request.form['email']
      psswrd=request.form['password']
      with dbapi2.connect(app.config['dsn']) as connection:
       cursor = connection.cursor()
      query= """ INSERT INTO MAINDATA(EMAIL,PASSWORD) VALUES ('%s','%s')"""  % (mssg,psswrd)
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
