from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import InputRequired


class SelectLocationForm(FlaskForm):
    """Form for selecting a state and a county."""
    State = SelectField("State: ", validators=[InputRequired()])
    