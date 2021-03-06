#This file extracts the information from the Census API and saves it in our database
from models import db, connect_db, Info, States
from app import app
import requests

db.drop_all()
db.create_all()

COUNTIES_API = 'https://api.census.gov/data/2019/acs/acsse?get=NAME&for=county:*&in=state:*&key=9459a79ef95b98b7009a83c5ba3d94c682f72e50'
STATES_API = 'https://api.covidactnow.org/v2/states.json?apiKey=b28cd827fcb9481db77660ed3eee9157'


# Extracting data for the information table
def information_table():
    """ Extracts information regarding a specific county including its county code, name and state"""

    res = requests.get(COUNTIES_API) 
    resp = res.json()
    length = len(resp)

    for y in range(1, length):
        county_state = resp[y][0].split(',')
        county_name = (county_state[0])
        state_name = (county_state[1])
        state_code = resp[y][1]
        county_code = resp[y][2]
        length1 = len(state_code)
        length2 = len(county_code)

        if(length1 == 1  & length2 == 1):
            joint_code = str(state_code) + str("0") + str(county_code)
        elif(length1 == 2 & length2 == 1):
            joint_code = str(state_code) +  str("0") + str(county_code)
        elif(length1 == 1 & length2 == 2):
            joint_code = str(state_code) + str(county_code)
        else:
            joint_code = str(state_code) + str(county_code)

        information = Info(county=county_name, state=state_name, county_code=county_code, state_code=state_code, joint_code=joint_code)
        db.session.add(information)
        db.session.commit()

def state_abb():
    """ seed states abbreviations into the database """

    res = requests.get(STATES_API)
    resp = res.json()

    for y in range(1, 53):
        states_abb = resp[y]['state']
        state_fips = resp[y]['fips']

        state = States(state=state_fips, state_abb=states_abb)
        db.session.add(state)
        db.session.commit()

#Calling all the functions defined above
information_table()
state_abb()