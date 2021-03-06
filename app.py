from flask import Flask, json, render_template, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import States, connect_db, db, Info
from forms import SelectLocationForm
import os
import requests

app = Flask(__name__, template_folder='Templates/')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgres:///covid_2')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY', 'secretkey')
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
toolbar = DebugToolbarExtension(app)

API_URL = 'https://api.covidactnow.org/v2/states.json?apiKey=b28cd827fcb9481db77660ed3eee9157'

@app.route('/')
def home_page():
    """ renders the home page with select field to choose a state"""

    form = SelectLocationForm()

    states = db.session.query(Info.state_code, Info.state).distinct().order_by(Info.state)
    form.State.choices = states

    return render_template('index.html', form=form)


@app.route('/county/<int:state_code>')
def states_page(state_code):
    """ returns all counties in that state """

    county = db.session.query(Info.county_code, Info.county).filter_by(state_code=state_code).order_by(Info.county).all()
    return jsonify(county)


@app.route('/demographics/<state>/<county>')
def demographics(state, county):
    """ returns demographic information regarding a county"""

    ED_API = f'https://api.census.gov/data/2019/acs/acsse?get=NAME,K201501_007E&for=county:{county}&in=state:{state}&key=9459a79ef95b98b7009a83c5ba3d94c682f72e50'
    POP_API = f'https://api.census.gov/data/2019/pep/population?get=DENSITY,POP&for=county:{county}&in=state:{state}&key=9459a79ef95b98b7009a83c5ba3d94c682f72e50'
    POV_API = f'https://api.census.gov/data/timeseries/poverty/saipe?get=NAME,SAEPOVRTALL_PT&for=county:{county}&in=state:{state}&key=9459a79ef95b98b7009a83c5ba3d94c682f72e50'

    res = requests.get(ED_API)
    resp = res.json()
    ed = resp[1][1]

    res2 = requests.get(POP_API)
    resp2 = res2.json()
    pop = resp2[1][1]
    pop_den = resp2[1][0]

    res3 = requests.get(POV_API)
    resp3 = res3.json()
    response_length = len(resp3)
    pov = resp3[response_length-1][1]

    return jsonify(ed, pop, pov, pop_den)


@app.route('/cases/<joint_code>')
def covid_cases(joint_code):
    """ returns covid cases regarding a specific county"""

    COVID_API = f'https://api.covidactnow.org/v2/county/{joint_code}.timeseries.json?apiKey=b28cd827fcb9481db77660ed3eee9157'
    res = requests.get(COVID_API)
    resp = res.json()
    return jsonify(resp)


@app.route('/cases/<int:state>/<int:county>')
def joint_code(state, county):
    """ helper function to return a joint_code of a specific county"""

    joint_code = db.session.query(Info.joint_code).filter_by(state_code=state, county_code=county).first()
    county_name = db.session.query(Info.county).filter_by(state_code=state, county_code=county).first()

    return jsonify(joint_code, county_name)


@app.route('/states')
def table_cases():
    """ returns covid information on a State level """

    res = requests.get(API_URL)
    resp = res.json()
    return jsonify(resp)


@app.route('/counties/<st_id>')
def counties_cases(st_id):
    """ returns covid information on a county level """

    state_abbreviation = db.session.query(States.state_abb).filter_by(state=str(st_id)).first()
    st = state_abbreviation.state_abb
    # print(jsonify(state_abbreviation))

    COUNTIES_API = f'https://api.covidactnow.org/v2/county/{st}.json?apiKey=b28cd827fcb9481db77660ed3eee9157'

    res = requests.get(COUNTIES_API)
    resp = res.json()
    return jsonify(resp)