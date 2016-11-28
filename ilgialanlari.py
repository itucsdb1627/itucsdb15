import datetime
from flask import redirect
from flask import request
from flask import flash
from flask import url_for
import psycopg2 as dbapi2
from flask import render_template
from config import app

class Grup:
    def __init__(self, GroupName, Explanation,StartDate, Sector):
        self.GroupName = GroupName
        self.Explanation = Explanation
        self.StartDate = StartDate
        self.Sector = Sector

@app.route('/ilgialanlari/init')
def init_groups_database():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    cursor.execute('''
    DROP TABLE IF EXISTS GRUP CASCADE;
    ''')
    query = """CREATE TABLE IF NOT EXISTS GRUP (
    ID SERIAL PRIMARY KEY,
    GROUPNAME VARCHAR(90) NOT NULL,
    EXPLANATION VARCHAR(300) NOT NULL,
    STARTDATE DATE NOT NULL,
    SECTOR VARCHAR(90) NOT NULL,
    PERSONID INTEGER,
    FOREIGN KEY (PERSONID)
    REFERENCES MAINDATA (ID)
    ON DELETE CASCADE)"""
    cursor.execute(query)
    connection.commit()
    return redirect(url_for('home_page'))


def add_groups(self, grup):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO GRUP (GROUPNAME, EXPLANATION, STARTDATE, SECTOR)
                    VALUES (%s, %s, %s, %s) """,
                    (grup.GroupName, grup.Explanation, grup.StartDate, grup.Sector))
                connection.commit()


@app.route('/ilgialanlari/<personid>', methods=['GET', 'POST'])
def ilgialanlari_page(personid):
    if request.method == 'GET':
        connection = dbapi2.connect(app.config['dsn'])
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM GRUP WHERE PERSONID = %s """,[personid])
        connection.commit()
        grup = [(key, GroupName,Explanation,StartDate,Sector,personid)
                        for key, GroupName, Explanation,StartDate ,Sector, personid in cursor]
        return render_template('ilgialanlari.html', grup = grup,personid=personid)


    else:
        if 'Add' in request.form:
            GroupName = request.form['GroupName']
            Explanation = request.form['Explanation']
            StartDate = request.form['StartDate']
            Sector = request.form['Sector']
            connection = dbapi2.connect(app.config['dsn'])
            cursor = connection.cursor()
            cursor.execute("""
            INSERT INTO GRUP (GROUPNAME, EXPLANATION,STARTDATE,SECTOR,PERSONID)
            VALUES (%s, %s, %s, %s, %s) """,
            (GroupName, Explanation,StartDate,Sector,personid))
            connection.commit()
            return redirect(url_for('ilgialanlari_page',personid=personid))

        elif 'Delete' in request.form:
            id = request.form['id']
            connection = dbapi2.connect(app.config['dsn'])
            cursor = connection.cursor()
            cursor.execute( """ DELETE FROM GRUP WHERE ID =%s """,[id])
            connection.commit()
            return redirect(url_for('ilgialanlari_page',personid=personid))
        elif 'Update' in request.form:
            grupid = request.form['id']
            return render_template('updategroups.html', key = grupid,personid=personid)
        elif 'Search' in request.form:
            GroupName = request.form['GroupName']
            connection = dbapi2.connect(app.config['dsn'])
            cursor = connection.cursor()
            cursor.execute( "SELECT * FROM GRUP WHERE GROUPNAME LIKE %s",(GroupName,))
            connection.commit()
            grup = [(key, GroupName,Explanation, StartDate, Sector,personid)
                        for key, GroupName, Explanation, StartDate, Sector,personid in cursor]
            return render_template('ilgialanlari.html',grup = grup,personid=personid)


@app.route('/ilgialanlari/updategroups/<grupid>,<personid>', methods=['GET', 'POST'])
def update_groups(grupid,personid):
    if request.method == 'GET':
        return render_template('updategroups.html')
    else:
         if 'Update' in request.form:
             GroupName = request.form['GroupName']
             Explanation = request.form['Explanation']
             StartDate = request.form['StartDate']
             Sector = request.form['Sector']
             connection = dbapi2.connect(app.config['dsn'])
             cursor = connection.cursor()
             cursor.execute(""" UPDATE GRUP SET GROUPNAME = %s, EXPLANATION= %s, STARTDATE= %s, SECTOR= %s WHERE ID = %s """,
             (GroupName, Explanation, StartDate, Sector, grupid))
             connection.commit()
             return redirect(url_for('ilgialanlari_page',personid=personid))

@app.route('/ilgialanlari/deletegroups')
def  delete_groups():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    cursor.execute("""DROP TABLE GRUP""" )
    connection.commit()
    return render_template('ilgialanlari.html')

