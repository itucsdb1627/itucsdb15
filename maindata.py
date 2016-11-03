import datetime
import os
import json
import re
import psycopg2 as dbapi2
from test.test_generators import email_tests

class maindata:
    def _init_(self,email,password):
       self.email=email
       self.password=password

def initialize_maindata_db(cursor):
    
   
    query=""" DROP TABLE IF EXISTS MAINDATA CASCADE"""
    cursor.execute(query)  
    query="""CREATE TABLE 
    MAINDATA(ID SERIAL PRIMARY KEY, EMAIL VARCHAR(50) NOT NULL,PASSWORD VARCHAR(50) NOT NULL,UNIQUE(EMAIL)"""
    cursor.execute(query)
    query="""INSERT INTO
    MAINDATA(EMAIL,PASSWORD) VALUES('simsekburak','1223334444')"""
    cursor.execute(query)
   