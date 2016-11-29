import datetime
from flask import redirect
from flask import request
from flask import flash
from flask import url_for
import psycopg2 as dbapi2
from flask import render_template
from config import app

class Network:
    def __init__(self, Il, Sirket, Sektor):
        self.Il = Il
        self.Sirket = Sirket
        self.Sektor = Sektor
       

@app.route('/network/db')
def init_network_database():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    cursor.execute('''
    DROP TABLE IF EXISTS KISILER CASCADE;
    ''')
    query = """CREATE TABLE IF NOT EXISTS NETWORK (
    ID SERIAL PRIMARY KEY,
    IL VARCHAR(90),
    SIRKET VARCHAR(30) NULL,
    PERSONID INTEGER,
    SEKTOR VARCHAR(30) NULL,
    FOREIGN KEY (PERSONID)
    REFERENCES MAINDATA (ID)
    ON DELETE CASCADE)"""
    cursor.execute(query)
    connection.commit()
    return redirect(url_for('home_page'))
     

def add_network(self, network):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO NETWORK (IL, SIRKET, SEKTOR)
                    VALUES (%s, %s, %s) """,
                    (network.Il, network.Sirket, network.Sektor))
                connection.commit()   
    

@app.route('/network/<personid>', methods=['GET', 'POST'])
def network_page(personid):
    if request.method == 'GET':
        connection = dbapi2.connect(app.config['dsn'])
        cursor = connection.cursor()
        cursor.execute("""select distinct a.*,b.schoolname,c.name from network a, education b,maindata c where a.personid=b.personid and  c.id=a.personid and  a.PERSONID = %s """,[personid])
        connection.commit()
        network = [(key, Il,Sirket,Personid ,Sektor,SchoolName,FirstName)
                        for key, Il,Sirket,Personid ,Sektor,SchoolName,FirstName in cursor]
        return render_template('network.html', network = network,personid=personid)
        
        
    else:
        if 'Add' in request.form:
            Il = request.form['Il']
            Sirket = request.form['Sirket']
            Sektor = request.form['Sektor']
            connection = dbapi2.connect(app.config['dsn'])
            cursor = connection.cursor()
            cursor.execute("""
            INSERT INTO NETWORK (IL, SIRKET,PERSONID,SEKTOR)
            VALUES (%s, %s, %s, %s) """,
            (Il,Sirket,personid ,Sektor))
            connection.commit()   
            return redirect(url_for('network_page',personid=personid))
        
        elif 'Delete' in request.form:
            id = request.form['id']
            connection = dbapi2.connect(app.config['dsn'])
            cursor = connection.cursor()
            cursor.execute( """ DELETE FROM NETWORK WHERE ID =%s """,[id])
            connection.commit()   
            return redirect(url_for('network_page',personid=personid))
        elif 'Update' in request.form:
            networkid = request.form['id']
            return render_template('network_edit.html', key = networkid,personid=personid)
        elif 'Search' in request.form:
            Il = request.form['Il']
            connection = dbapi2.connect(app.config['dsn'])
            cursor = connection.cursor()
            cursor.execute( "SELECT * FROM NETWORK WHERE IL LIKE %s",(Il,))
            connection.commit() 
            network = [(key, Il,Sirket,Personid ,Sektor)
                        for key, Il,Sirket,Personid ,Sektor in cursor]
            return render_template('network.html',network = network,personid=personid)   
        
        
@app.route('/network/editnetwork/<networkid>,<personid>', methods=['GET', 'POST'])
def edit_network(networkid,personid):
    if request.method == 'GET': 
        return render_template('network_edit.html')
    else:
         if 'Update' in request.form:
             Il = request.form['Il']
             Sirket = request.form['Sirket']
             Sektor = request.form['Sektor']
             connection = dbapi2.connect(app.config['dsn'])
             cursor = connection.cursor()
             cursor.execute(""" UPDATE NETWORK SET IL = %s, SIRKET= %s, SEKTOR= %s WHERE ID = %s """,
             (Il,Sirket,Sektor , networkid))
             connection.commit()   
             return redirect(url_for('network_page',personid=personid))
             
@app.route('/network/deletedb')
def  deletenetwork_db():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    cursor.execute("""DROP TABLE NETWORK""" )
    connection.commit()
    return render_template('network.html')

