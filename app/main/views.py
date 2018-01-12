from flask import render_template, send_from_directory, request, jsonify, redirect, url_for
from .form import ProjectForm
from ..models import Project
from .. import db
from . import main
import os
from time import sleep

@main.route("/", methods=["GET","POST"])
def index():
    showLink = {"showIpaLink":True,"showAndroidLink":True,"showiOSLink":True}
    userAgent = request.headers.get("User-Agent")
    if any(agent in userAgent for agent in ["iPhone","iPad"]):
        showLink["showIpaLink"] = False
        showLink["showAndroidLink"] = False
    elif "Android" in userAgent:
        showLink["showIpaLink"] = False
        showLink["showiOSLink"] = False
    appList = [1,2,3]
    return render_template('index.html', appList=appList, showLink=showLink)

@main.route("/admin", methods=["GET","POST"])
def admin():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(name=form.name.data, version=form.version.data, description=form.description.data, jenkins_url=form.jenkins_url.data)
        db.session.add(project)
        print("xxx")
        return redirect(url_for("main.admin"))
    form.name.data = ""
    form.version.data = ""
    form.description.data = ""
    form.jenkins_url.data = ""    
    projectList = Project.query.all()
    return render_template("admin.html",projectList=projectList)


@main.route("/createProject", methods=["GET","POST"])
def createProject():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(name=form.name.data, version=form.version.data, description=form.description.data, jenkins_url=form.jenkins_url.data)
        db.session.add(project)
        return jsonify(status='ok')
    form.name.data = ""
    form.version.data = ""
    form.description.data = ""
    form.jenkins_url.data = ""
    return render_template("project.html",form=form)


@main.route("/download/<filename>", methods=["GET","POST"])
def download(filename):
    directory =os.path.join(os.getcwd(),"store") 
    return send_from_directory(directory, filename, as_attachment=True)