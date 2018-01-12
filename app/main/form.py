from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import DataRequired

class ProjectForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    version = StringField("Version", validators=[DataRequired()])
    description = TextAreaField("Description")
    jenkins_url = StringField("Jenkins Url", validators=[DataRequired()])
    submit = SubmitField("Save")