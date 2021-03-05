from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Info(db.Model):
    __tablename__ = 'info'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    county = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(80), nullable=False)
    county_code = db.Column(db.Integer, nullable=False)
    state_code = db.Column(db.Integer, nullable=False)
    joint_code = db.Column(db.String, nullable=False, unique=True)
    
    def __repr__(self):
        return f"<Info {self.id} state={self.state} county={self.county} state_code={self.state_code} county_code={self.county_code} joint_code={self.joint_code}>"

class Education(db.Model):
    __tablename__ = 'education'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    county_code = db.Column(db.Integer, nullable=False)
    state_code = db.Column(db.Integer, nullable=False)
    ed_pop = db.Column(db.Integer, nullable=True)

class Population(db.Model):
    __tablename__ = 'population'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    county_code = db.Column(db.Integer, nullable=False)
    state_code = db.Column(db.Integer, nullable=False)
    pop = db.Column(db.Float, nullable=True)
    pop_den = db.Column(db.Float, nullable=True)

class Poverty(db.Model):
    __tablename__ = 'poverty'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    county_code = db.Column(db.Integer, nullable=False)
    state_code = db.Column(db.Integer, nullable=False)
    pov = db.Column(db.Float, nullable=True)

# DO NOT MODIFY THIS FUNCTION
def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
