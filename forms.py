from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    FloatField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Email
)


class RegisterForm(FlaskForm):

    name = StringField(
        "Name",
        validators=[DataRequired()]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired()]
    )

    submit = SubmitField(
        "Register"
    )


class LoginForm(FlaskForm):

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired()]
    )

    submit = SubmitField(
        "Login"
    )


class CarbonForm(FlaskForm):

    electricity = FloatField(
        "Electricity",
        validators=[DataRequired()]
    )

    vehicle = FloatField(
        "Vehicle",
        validators=[DataRequired()]
    )

    flights = FloatField(
        "Flights",
        validators=[DataRequired()]
    )

    submit = SubmitField(
        "Calculate"
    )