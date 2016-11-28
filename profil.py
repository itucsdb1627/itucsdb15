import datetime
from flask import redirect
from flask import request
from flask import flash
from flask import url_for
import psycopg2 as dbapi2
from flask import render_template
from config import app

from education import *
from experience import *
from profilpicture import *
from language import *


class Education:
    def __init__(self, SchoolName, Year, Gpa):
        self.SchoolName = SchoolName
        self.Year = Year
        self.Gpa = Gpa
       


     

def add_education(self, education):
        with dbapi2.connect(self.app.config['dsn']) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO EDUCATION (SCHOOLNAME, YEAR, GPA)
                    VALUES (%s, %s, %s) """,
                    (education.SchoolName, education.Year, education.Gpa))
                connection.commit()   
    

@app.route('/profil/<personid>', methods=['GET', 'POST'])
def profil_page(personid):
    if request.method == 'GET':
        education = showeducation_page(personid)
        experience = showexperience_page(personid)
        language  = showlanguage(personid)
        return render_template('profil.html', education = education,experience=experience,language=language,personid=personid)

    else:
            
        if 'Add' in request.form:
                addeducation_page(personid)  
                return redirect(url_for('profil_page',personid=personid))
                        
        elif 'Delete' in request.form:
                deleteeducation_page(personid)  
                return redirect(url_for('profil_page',personid=personid))
                
        elif 'Update' in request.form:
                educationid=updateeducation_page(personid)
                return render_template('education_edit.html', key = educationid,personid=personid)
                
        elif 'Search' in request.form:
                education=searcheducation_page(personid)
                return render_template('profil.html',education = education,personid=personid)
            
        elif 'AddExperience' in request.form:
                addexperience_page(personid)  
                return redirect(url_for('profil_page',personid=personid)) 
            
        elif 'DeleteExperience' in request.form:
                deleteexperience_page(personid)  
                return redirect(url_for('profil_page',personid=personid)) 
            
        elif 'UpdateExperience' in request.form:
                experienceid=updateexperience_page(personid)
                return render_template('experience_edit.html', key = experienceid,personid=personid)
            
        elif 'SearchExperience' in request.form:
                experience=searchexperience_page(personid)
                return render_template('profil.html',experience = experience,personid=personid)
            
        elif 'AddLanguage' in request.form:
                addlanguage(personid)  
                return redirect(url_for('profil_page',personid=personid)) 
        elif 'DeleteLanguage' in request.form:
                deletelanguage(personid)  
                return redirect(url_for('profil_page',personid=personid)) 
            
        elif 'UpdateLanguage' in request.form:
                languageid=updateexperience_page(personid)
                return render_template('language_edit.html', key = languageid,personid=personid)
          
        elif 'SearchLanguage' in request.form:
                language=searchlanguage(personid)
                return render_template('profil.html',language = language,personid=personid)