import datetime
from flask import redirect
from flask import request
from flask import flash
from flask import url_for
import psycopg2 as dbapi2
from flask import render_template
from config import app


@app.route('/baglantilar/initdb')
def initialize_friendrequest_db():
    connection=dbapi2.connect(app.config['dsn'])
    cursor=connection.cursor()
    query=""" DROP TABLE IF EXISTS LOCATION CASCADE"""
    cursor.execute(query)
    query="""CREATE TABLE FRIENDREQUEST(PERSONID INTEGER,REQUESTID INTEGER,FOREIGN KEY (PERSONID) REFERENCES MAINDATA(ID) ON DELETE CASCADE ON UPDATE CASCADE )"""
    cursor.execute(query)
    connection.commit()
    return redirect(url_for('baglantilar_page'))


@app.route('/baglantilar/<personid>', methods=['GET', 'POST'])
def baglantilar_page(personid):
    if request.method=='GET':
        connection=dbapi2.connect(app.config['dsn'])
        cursor=connection.cursor()
        cursor.execute("""SELECT * FROM MAINDATA WHERE %s!=MAINDATA.ID ORDER BY  EMAIL""",(personid))
        backupmaindata=cursor.fetchall()
        connection.commit()
        maindata = [(key,email,password,name,surname)
                for key,email,password,name,surname in cursor]
        
    
       
        connection = dbapi2.connect(app.config['dsn'])
        cursor = connection.cursor()
        cursor.execute("""
        SELECT * FROM  FRIENDREQUEST WHERE REQUESTID=%s""",(personid,))
        backupmaindata2=cursor.fetchall()
        connection.commit()
        maindata2 = [(key,requestid)
                for key,requestid in cursor]
        
        return render_template('baglantilar.html',personid=personid,maindata=backupmaindata,maindata2=backupmaindata2)
        
        
        
    else:

      if 'AddRequest' in request.form:
            key = request.form['id']
            connection = dbapi2.connect(app.config['dsn'])
            cursor = connection.cursor()
            cursor.execute("""
            INSERT INTO FRIENDREQUEST (PERSONID,REQUESTID)
            VALUES (%s, %s) """,
            (personid,key,))
            connection.commit()
            return redirect(url_for('baglantilar_page',personid=personid))
      elif 'DeleteRequest' in request.form:
            key = request.form['id']
            connection = dbapi2.connect(app.config['dsn'])
            cursor = connection.cursor()
            cursor.execute("""DELETE FROM FRIENDREQUEST WHERE PERSONID=%s AND REQUESTID=%s""",(personid,key,))
            connection.commit()
            return redirect(url_for('baglantilar_page',personid=personid))

   