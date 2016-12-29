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





        connection=dbapi2.connect(app.config['dsn'])
        cursor=connection.cursor()
        cursor.execute("""SELECT FRIENDREQUEST.PERSONID,MAINDATA.NAME,MAINDATA.SURNAME
        FROM FRIENDREQUEST INNER JOIN MAINDATA ON FRIENDREQUEST.PERSONID=MAINDATA.ID WHERE REQUESTID=%s""",(personid))
        backupmaindata4=cursor.fetchall()
        connection.commit()
        maindata4=[(key2,name,surname)
                    for key2,name,surname in cursor]

        connection = dbapi2.connect(app.config['dsn'])
        cursor = connection.cursor()
        cursor.execute("""
        SELECT FRIENDLIST.FRIENDID,MAINDATA.ID,MAINDATA.NAME,MAINDATA.SURNAME,FRIENDLIST.TITLE FROM  FRIENDLIST INNER JOIN MAINDATA ON FRIENDLIST.FRIENDID=MAINDATA.ID WHERE PERSONID=%s""",(personid,))
        backupmaindata3=cursor.fetchall()
        connection.commit()
        maindata3 = [(key1,requestid,name,surname,title)
                for key1,requestid,name,surname,title in cursor]

        return render_template('baglantilar.html',personid=personid,maindata=backupmaindata,maindata3=backupmaindata3,maindata4=backupmaindata4)



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
            cursor.execute("""DELETE FROM FRIENDREQUEST WHERE PERSONID=%s AND REQUESTID=%s""",(key,personid,))
            connection.commit()
            return redirect(url_for('baglantilar_page',personid=personid))
      elif 'AddFriend' in request.form:
            key = request.form['id']
            title=request.form['title']
            connection = dbapi2.connect(app.config['dsn'])
            cursor = connection.cursor()
            cursor.execute("""
            INSERT INTO FRIENDLIST (PERSONID,FRIENDID,TITLE)
            VALUES (%s, %s ,%s) """,
            (personid,key,title))
            cursor.execute("""DELETE FROM FRIENDREQUEST WHERE PERSONID=%s AND REQUESTID=%s""",(key,personid,))
            cursor.execute("""
            INSERT INTO FRIENDLIST (PERSONID,FRIENDID)
            VALUES (%s, %s) """,
            (key,personid,))
            connection.commit()
            return redirect(url_for('baglantilar_page',personid=personid))

      elif 'DeleteFriend' in request.form:
            key = request.form['id']
            connection = dbapi2.connect(app.config['dsn'])
            cursor = connection.cursor()
            cursor.execute("""
            DELETE FROM FRIENDLIST WHERE PERSONID=%s AND FRIENDID=%s
             """,
            (personid,key,))
            cursor.execute("""
            DELETE FROM FRIENDLIST WHERE PERSONID=%s AND FRIENDID=%s
             """,
            (key,personid,))

            connection.commit()
            return redirect(url_for('baglantilar_page',personid=personid))

@app.route('/baglantilar/update/<personid>,<requestid>', methods=['GET', 'POST'])
def baglantilar_guncelle(personid,requestid):



        return render_template('baglantilarupdate.html',personid=personid,requestid=requestid)

@app.route('/baglantilar/titleguncelle/<personid>,<requestid>', methods=['GET', 'POST'])
def title_guncelle(personid,requestid):
         title=request.form['title']
         connection = dbapi2.connect(app.config['dsn'])
         cursor = connection.cursor()
         cursor.execute("""UPDATE FRIENDLIST SET TITLE=%s WHERE PERSONID= %s AND FRIENDID=%s""" ,(title,personid,requestid))
         connection.commit()

         return redirect(url_for('baglantilar_page',personid=personid))



