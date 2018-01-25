from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField,FileAllowed,FileRequired
from ..models import Project
from .. import store
import os

class ProjectForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    version = StringField("Version", validators=[DataRequired()])
    description = TextAreaField("Description")
    android_jenkins_url = StringField("Android Jenkins Url")
    ios_jenkins_url = StringField("iOS Jenkins Url")
    plist = FileField("iOS Plist File")
    @staticmethod
    def getProjectID(id):
        global projectID 
        projectID = id

    def validate(self):
        rv = FlaskForm.validate(self)
        print(projectID)
        if not rv:
            return False
        if int(projectID)!=0:
            project1 = Project.query.get_or_404(int(projectID))
            project2 = Project.query.filter_by(name=self.name.data,version=self.version.data).first()
            if project2 and (project1.name!=self.name.data or project1.version!=self.version.data):
                self.name.errors.append('Mobile project was existed with %s-%s'%(self.name.data,self.version.data))
                return False
        else:
            project = Project.query.filter_by(name=self.name.data,version=self.version.data).first()
            if project:
                self.name.errors.append('Mobile project was existed with %s-%s'%(self.name.data,self.version.data))
                return False
        return True
