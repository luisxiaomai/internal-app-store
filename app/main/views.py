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
    
    projectList = Project.query.all()
    return render_template("admin.html",projectList=projectList)

@main.route("/createProject", methods=["GET","POST"])
def createProject():
    form = ProjectForm()
    if form.validate_on_submit():
        id = int(request.form["id"]) 
        if id==0:
            project = Project(name=form.name.data, version=form.version.data, description=form.description.data, android_jenkins_url=form.android_jenkins_url.data,ios_jenkins_url=form.ios_jenkins_url.data)
        else:
            project = Project.query.get_or_404(id)
            project.name = form.name.data
            project.version = form.version.data
            project.description = form.description.data
            project.android_jenkins_url = form.android_jenkins_url.data
            project.ios_jenkins_url = form.ios_jenkins_url.data

        db.session.add(project)
        return jsonify(status='ok')
    if len(request.args)!=0:
        project = Project.query.get_or_404(request.args.get("id"))
        form.name.data = project.name
        form.version.data = project.version
        form.description.data = project.description
        form.android_jenkins_url.data = project.android_jenkins_url
        form.ios_jenkins_url.data = project.ios_jenkins_url
        return render_template("project.html",form=form,projectID=project.id)
    else:
        return render_template("project.html",form=form)

@main.route("/deleteProject", methods=["GET","POST"])
def deleteProject():
    if request.method == 'POST':
        print(request.args.get("id"))
        project = Project.query.get_or_404(int(request.form["id"]))
        db.session.delete(project)
        return jsonify(status='ok')

@main.route("/download/<filename>", methods=["GET","POST"])
def download(filename):
    directory =os.path.join(os.getcwd(),"store") 
    return send_from_directory(directory, filename, as_attachment=True)