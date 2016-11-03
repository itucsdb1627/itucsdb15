import datetime
import os
import json
import re
import psycopg2 as dbapi2



class Education:
    def __init__(self, SchoolName, Year, Gpa):
        self.SchoolName = SchoolName
        self.Year = Year
        self.Gpa = Gpa
       

def init_education_database(cursor):
    
    query = """CREATE TABLE IF NOT EXISTS EDUCATION (
    ID SERIAL PRIMARY KEY,
    SCHOOLNAME VARCHAR(90),
    YEAR VARCHAR(30) NULL,
    GPA VARCHAR(30) NULL)"""
    
    cursor.execute(query)
    fill_education_db(cursor)
    
def fill_education_db(cursor):
    query = """
    INSERT INTO EDUCATION (SCHOOLNAME, YEAR, GPA) VALUES ('Istanbul Teknik Universitesi', '2007-2001', '85');
    INSERT INTO EDUCATION (SCHOOLNAME, YEAR, GPA) VALUES ('Denizli Anadolu Lisesi', '2011-2016', '3.00' );"""

    cursor.execute(query)               

def add_education(self, education):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO EDUCATION (SCHOOLNAME, YEAR, GPA)
                    VALUES (%s, %s, %s) """,
                    (education.SchoolName, education.Year, education.Gpa))
                connection.commit()   
    



