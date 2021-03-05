from logging import info
from unittest import TestCase
from app import app
from models import db, Info, Education, Population, Poverty
from flask import request

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///covid_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

db.drop_all()
db.create_all()

# Setting up inital values
ed = Education(county_code='017', state_code=39, ed_pop=51551)
population = Population(county_code='017', state_code=39, pop=383134, pop_den=821)
poverty = Poverty(county_code='017', state_code=39, pov=10)


class informationTestCase(TestCase):

    def setUp(self):

        Info.query.delete()
        Education.query.delete()
        Population.query.delete()
        Poverty.query.delete()

        information = Info(county='Butler County', state='Ohio', county_code='017', state_code=39, joint_code=39017)
        education = Education(county_code='017', state_code=39, ed_pop=54151)
        population = Population(county_code='017', state_code=39, pop=384134, pop_den=821)
        poverty = Poverty(county_code='017', state_code=39, pov=11.7)

        db.session.add_all([information, education, population, poverty])
        db.session.commit()

        self.information = information
        self.education = education
        self.population = population
        self.poverty = poverty

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()

        db.session.delete(self.information)
        db.session.delete(self.education)
        db.session.delete(self.population)
        db.session.delete(self.poverty)

    def test_home_page(self):
        with app.test_client() as client:
            """ returns all counties in that state """

            resp = client.get('/')

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2 class="h2 text">Select Location</h2>', str(resp.data))
            self.assertIn('<h2 class="h2 text text-center"> County Demographics</h2>', str(resp.data))
            self.assertIn('<h2 class="mt-5 h2 text">States Covid Cases Comparision</h2>', str(resp.data))


    def test_states_page(self):
        with app.test_client() as client:
            """ returns all counties in that state """
            url = '/county/39'
            resp = client.get(url)
            data = resp.json

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(data, [[17, 'Butler County']])


    def test_demographics(self):
        with app.test_client() as client:
            """ returns demographic information regarding a county"""

            url = '/demographics/39/017'
            response = client.get(url)
            data = response.json

            self.assertEqual(response.status_code, 200)
            self.assertEqual(data, [[ 54151 ], [ 384134, 821],[ 11.7 ]])


    def test_covid_cases(self):
        with app.test_client() as client:
            """ returns covid cases regarding a specific county"""

            url = '/cases/39017'
            response = client.get(url)

            self.assertEqual(response.status_code, 200)
            self.assertIn('"cases": 35496,', str(response.data))


    def test_joint_code(self):
        with app.test_client() as client:
            """ returns covid cases regarding a specific county"""

            url = '/cases/39/17'
            response = client.get(url)
            data = response.json

            self.assertEqual(response.status_code, 200)
            self.assertEqual(data, [["39017"], ["Butler County"] ])


    def test_table_cases(self):
        with app.test_client() as client:
            """ returns covid information on a State level """
            url = '/states'
            res = client.get(url)
            data = res.json

            self.assertEqual(res.status_code, 200)
            self.assertIn('AK', str(data))
        