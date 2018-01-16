from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField
from wtforms.validators import DataRequired
from ..models import Project

class ProjectForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    version = StringField("Version", validators=[DataRequired()])
    description = TextAreaField("Description")
    android_jenkins_url = StringField("Android Jenkins Url")
    ios_jenkins_url = StringField("iOS Jenkins Url")

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False
        project = Project.query.filter_by(name=self.name.data,version=self.version.data).first()
        if project:
            self.name.errors.append('Mobile project was existed with %s-%s'%(self.name.data,self.version.data))
            return False
        return True
