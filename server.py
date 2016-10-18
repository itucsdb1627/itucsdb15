import datetime
import os

from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def home_page():
    now = datetime.datetime.now()
    return render_template('home.html', current_time=now.ctime())

@app.route('/ilgialanlari')
def ilgialanlari_page():
    return render_template('ilgialanlari.html')
@app.route('/kisiler')
def kisiler_page():
    return render_template('kisiler.html')
@app.route('/baglantilar')
def baglantilar_page():
    return render_template('baglantilar.html')
@app.route('/hakkimizda')
def hakkimizda_page():
    return render_template('hakkimizda.html')
@app.route('/isfirsatlari')
def isfirsatlari_page():
    return render_template('isfirsatlari.html')

if __name__ == '__main__':
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5001, True
    app.run(host='0.0.0.0', port=5001, debug=debug)
