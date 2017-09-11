from flask_wtf import FlaskForm as Form
from wtforms import TextField, TextAreaField, SubmitField, validators, ValidationError, PasswordField
from app.intro_to_flask.models import db, User


class ContactForm(Form):
    name = TextField("Name", [validators.DataRequired("Please enter your name.")])
    email = TextField("Email", [validators.DataRequired("Please enter your email address."),
                                validators.Email("Please enter your email address.")])
    subject = TextField("Subject", [validators.DataRequired("Please enter a subject.")])
    message = TextAreaField("Message", [validators.DataRequired("Please enter a message.")])
    submit = SubmitField("Send")


class SignupForm(Form):
    firstname = TextField("First name", [validators.DataRequired("Please enter your first name.")])
    lastname = TextField("Last name", [validators.DataRequired("Please enter your last name.")])
    email = TextField("Email", [validators.DataRequired("Please enter your email address."),
                                validators.Email("Please enter your email address.")])
    password = PasswordField('Password', [validators.DataRequired("Please enter a password.")])
    submit = SubmitField("Create account")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(email=self.email.data.lower()).first()
        if user:
            self.email.errors.append("That email is already taken")
            return False
        else:
            return True


class SigninForm(Form):
    email = TextField("Email", [validators.Required("Please enter your email address."),
                                validators.Email("Please enter your email address.")])
    password = PasswordField('Password', [validators.Required("Please enter a password.")])
    submit = SubmitField("Sign In")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(
            email=self.email.data.lower()).first()
        if user is None:
            self.email.errors.append('Unknown me')
            return False

        if not user.check_password(self.password.data.lower()):
            self.password.errors.append('Invalid password')
            return False

        self.user = user
        return True



        """user = User.query.filter_by(email=self.email.data.lower()).first()
        if user and user.check_password(self.password.data):  # Something wrong with password checking, user is fine.
            return True
        else:
            self.email.errors.append("Invalid e-mail or password" + self.password.data)
            return False"""
