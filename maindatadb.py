import datetime
from flask import redirect
from flask import request
from flask import flash
from flask import url_for
import psycopg2 as dbapi2
from flask import render_template
from config import app

@app.route('/admin/initdb')
def initialize_maindata_db():
    connection=dbapi2.connect(app.config['dsn'])
    cursor=connection.cursor()

    query=""" DROP TABLE IF EXISTS MAINDATA CASCADE"""
    cursor.execute(query)
    query="""CREATE TABLE MAINDATA(ID SERIAL PRIMARY KEY, EMAIL VARCHAR(50) NOT NULL,PASSWORD VARCHAR(50) NOT NULL,NAME VARCHAR(50) NOT NULL,SURNAME VARCHAR(50) NOT NULL,UNIQUE(EMAIL))"""
    cursor.execute(query)
    query="""INSERT INTO MAINDATA(EMAIL,PASSWORD,NAME,SURNAME) VALUES('simsekburak','asd','Burak','Simsek')"""
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
          maindata = [(key,email,password,name,surname)
                 for key,email,password,name,surname in cursor]
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
      backupmaindata=[(key,email,password,name,surname)
                      for key,email,password,name,surname in cursor]

      return render_template('updateuser.html',backupmaindata=backupmaindata)
@app.route('/admin/updateuser/<asdid>',methods=['POST','GET'])
def update_user(asdid):
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    if request.method=='POST':

       posta=request.form['email']
       psswd=request.form['password']
       name=request.form['name']
       surname=request.form['surname']
       cursor.execute("""UPDATE MAINDATA SET EMAIL=%s,PASSWORD=%s,NAME=%s,SURNAME=%s  WHERE ID= %s""" ,(posta,psswd,name,surname,asdid))
       connection.commit()

       return redirect(url_for('admin_page'))
    elif request.method=='GET':
        return render_template('updateuser.html')
@app.route('/admin/delete')
def  deleteadmin_db():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    cursor.execute("""DROP TABLE MAINDATA""" )
    connection.commit()
    return render_template('admin.html')