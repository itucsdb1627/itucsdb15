import datetime
from flask import redirect
from flask import request
from flask import flash
from flask import url_for
import psycopg2 as dbapi2
from flask import render_template
from config import app

from grup import *
from publishes import *
from activities import *

class Grup:
    def __init__(self, GroupName, Explanation,StartDate, Sector):
        self.GroupName = GroupName
        self.Explanation = Explanation
        self.StartDate = StartDate
        self.Sector = Sector


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
        grup=expressgrup_page(personid)
        publishes=expresspublishes_page(personid)
        activities=expressactivities_page(personid)
        return render_template('ilgialanlari.html',grup=grup,publishes=publishes,activities=activities,personid=personid)

    else:
        if 'Addpublishes' in request.form:
            addpublishes_page(personid)
            return redirect(url_for('ilgialanlari_page',personid=personid))
        elif 'Add' in request.form:
            addgrup_page(personid)
            return redirect(url_for('ilgialanlari_page',personid=personid))
        elif 'Addactivities' in request.form:
            addactivities_page(personid)
            return redirect(url_for('ilgialanlari_page',personid=personid))
        elif 'Deletepublishes' in request.form:
            deletepublishes_page(personid)
            return redirect(url_for('ilgialanlari_page',personid=personid))
        elif 'Delete' in request.form:
            deletegrup_page(personid)
            return redirect(url_for('ilgialanlari_page',personid=personid))
        elif 'Deleteactivities' in request.form:
            deleteactivities_page(personid)
            return redirect(url_for('ilgialanlari_page',personid=personid))
        elif 'Updatepublishes' in request.form:
            publishesid=updatepublishes_page(personid)
            return render_template('updatepublishes.html', key = publishesid,personid=personid)
        elif 'Update' in request.form:
            grupid=updategrup_page(personid)
            return render_template('updategroups.html', key = grupid,personid=personid)
        elif 'Updateactivities' in request.form:
            activitiesid=updateactivities_page(personid)
            return render_template('updateactivities.html', key = activitiesid,personid=personid)
        elif 'Searchpublishes' in request.form:
            publishes=searchpublishes_page(personid)
            return render_template('ilgialanlari.html',publishes=publishes,personid=personid)
        elif 'Search' in request.form:
            grup=searchgrup_page(personid)
            return render_template('ilgialanlari.html',grup = grup,personid=personid)
        elif 'Searchactivities' in request.form:
            activities=searchactivities_page(personid)
            return render_template('ilgialanlari.html',activities = activities,personid=personid)

