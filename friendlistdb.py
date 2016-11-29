import datetime
from flask import redirect
from flask import request
from flask import flash
from flask import url_for
import psycopg2 as dbapi2
from flask import render_template
from config import app


@app.route('/baglantilar/initfrienddb')
def initialize_friendlist_db():
    connection=dbapi2.connect(app.config['dsn'])
    cursor=connection.cursor()
    query=""" DROP TABLE IF EXISTS LOCATION CASCADE"""
    cursor.execute(query)
    query="""CREATE TABLE FRIENDLIST(PERSONID INTEGER,FRIENDID INTEGER,TITLE VARCHAR(50), FOREIGN KEY (PERSONID) REFERENCES MAINDATA(ID) ON DELETE CASCADE ON UPDATE CASCADE )"""
    cursor.execute(query)
    connection.commit()
    return redirect(url_for('baglantilar_page'))

