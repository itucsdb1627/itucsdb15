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
from language import *


class Education:
    def __init__(self, SchoolName, Year, Gpa):
        self.SchoolName = SchoolName
        self.Year = Year
        self.Gpa = Gpa
       


    

@app.route('/profil/<personid>', methods=['GET', 'POST'])
def profil_page(personid):
    if request.method == 'GET':
        education = showeducation_page(personid)
        experience = showexperience_page(personid)
        language  = showlanguage(personid)
        return render_template('profil.html', education = education,experience=experience,language=language,personid=personid)

    else:
            
        if 'AddEducation' in request.form:
                addeducation_page(personid)  
                return redirect(url_for('profil_page',personid=personid))
                        
        elif 'DeleteEducation' in request.form:
                deleteeducation_page(personid)  
                return redirect(url_for('profil_page',personid=personid))
                
        elif 'UpdateEducation' in request.form:
                educationid=updateeducation_page(personid)
                UpdateEducationValue = show_education_update_value(educationid);
                return render_template('education_edit.html', key = educationid,personid=personid,UpdateEducationValue=UpdateEducationValue)
                
        elif 'SearchEducation' in request.form:
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
                UpdateExperienceValue=show_experience_update_value(experienceid)
                return render_template('experience_edit.html', key = experienceid,personid=personid,UpdateExperienceValue=UpdateExperienceValue)
            
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
                UpdateLanguageValue=show_language_update_value(languageid)
                return render_template('language_edit.html', key = languageid,personid=personid,UpdateLanguageValue=UpdateLanguageValue)
          
        elif 'SearchLanguage' in request.form:
                language=searchlanguage(personid)
                return render_template('profil.html',language = language,personid=personid)