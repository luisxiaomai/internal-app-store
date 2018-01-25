from flask import render_template, send_from_directory, request, jsonify, redirect, url_for, make_response, send_file, current_app
from .form import ProjectForm
from ..models import Project
from .. import db, store
from . import main
import os, time, shutil, glob, subprocess
from subprocess import call
import threading
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
users = [{"username":"admin","password":"test"}]
@auth.get_password
def get_password(username):
    for user in users:
        if user["username"]== username:
            return user["password"]
    return None

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
    projectList = Project.query.all()
    # Append app latest update time
    for project in projectList:
        folderName = "%s-%s"%(project.name,project.version)
        directory =os.path.join(current_app.config["UPLOADED_STORE_DEST"] ,folderName) 

        for file in os.listdir(directory):
            if file.endswith(".ipa"):
                setattr(project, "iOSUpdateTime",time.ctime(os.path.getmtime(os.path.join(directory,file))))
            elif file.endswith(".apk"):
                setattr(project, "androidUpdateTime",time.ctime(os.path.getmtime(os.path.join(directory,file))))
        if not hasattr(project,"iOSUpdateTime"):
            setattr(project, "iOSUpdateTime",None)
        if not hasattr(project,"androidUpdateTime"):
            setattr(project, "androidUpdateTime",None)
    return render_template('index.html', projectList=projectList, showLink=showLink)
    
@main.route("/installCA", methods=["GET","POST"])
def installCA():
    print(current_app.config["UPLOADED_STORE_DEST"])
    return send_from_directory(current_app.config["UPLOADED_STORE_DEST"], "ca.crt", as_attachment=True)

@main.route("/admin", methods=["GET","POST"])
@auth.login_required
def admin():
    form = ProjectForm()
    projectList = Project.query.all()
    return render_template("admin.html",projectList=projectList)

@main.route("/testSync", methods=["GET","POST"])
def testSync():
    form = ProjectForm()
    projectList = Project.query.all()
    return render_template("test.html",projectList=projectList)

@main.route("/createProject", methods=["GET","POST"])
def createProject():
    form = ProjectForm()
    form.getProjectID(request.form.get("id",0))
    if form.validate_on_submit():
        id = int(request.form["id"]) 
        plist_name = ""
        plist_url = ""
        folderName = "%s-%s"%(form.name.data,form.version.data)
        if form.plist.data:
            plist_name = store.save(form.plist.data, name ="%s/"%folderName +  folderName + "." )
            plist_url = store.url(plist_name)
        if id==0:
            project = Project(name=form.name.data, version=form.version.data, description=form.description.data, android_jenkins_url=form.android_jenkins_url.data,ios_jenkins_url=form.ios_jenkins_url.data, plist_name=plist_name, plist_url=plist_url)
        else:
            project = Project.query.get_or_404(id)
            project.name = form.name.data
            project.version = form.version.data
            project.description = form.description.data
            project.android_jenkins_url = form.android_jenkins_url.data
            project.ios_jenkins_url = form.ios_jenkins_url.data
            project.plist_name=plist_name
            project.plist_url =plist_url
        #create related folder
        try:
            directory =os.path.join(current_app.config["UPLOADED_STORE_DEST"] ,folderName) 
            if not os.path.exists(directory):
                os.makedirs(directory)
        except OSError:
            print ('Error: Creating directory. ' +  directory)
        db.session.add(project)
        return jsonify(status='ok')
    if int(request.args.get("id",0)) != 0 or int(request.form.get("id",0)) != 0:
        projectID = request.args.get("id",0) if  request.args.get("id",0) else request.form.get("id",0)
        project = Project.query.get_or_404(int(projectID))
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
        #delete related folder
        folderName = "%s-%s"%(project.name,project.version)
        directory =os.path.join(current_app.config["UPLOADED_STORE_DEST"] ,folderName) 
        if os.path.exists(directory):
            shutil.rmtree(directory)
        return jsonify(status='ok')

@main.route("/download", methods=["GET","POST"])
def download():
    project = Project.query.get_or_404(request.args.get("projectID"))
    folderName = "%s-%s"%(project.name,project.version)
    directory =os.path.join(current_app.config["UPLOADED_STORE_DEST"] ,folderName) 
    type = request.args.get("type")
    for file in os.listdir(directory):
        if file.endswith(".ipa") and type == "ipa":
            filename = file
            break
        elif file.endswith(".apk") and type == "apk":
            filename = file
            break
        elif type == "iOS":
            return "itms-services://?action=download-manifest&url=https://127.0.0.1:5000/static/anwstream.plist"
        else:
            filename = None
    return send_from_directory(directory, filename, as_attachment=True)


@main.route("/sync", methods=["GET","POST"])
def sync():
    print("start sync")
    t = threading.Thread(target=startTask, args=[current_app._get_current_object()])
    t.daemon = True
    t.start()
    print("return sync status")
    return jsonify(status='ok')

@main.route("/getIPA", methods=["GET","POST"])
def getIPA():
    response = make_response(send_file("anwstream.ipa"))
    response.headers["Content-Disposition"] = "attachment;filename=anwstream.ipa;"
    return response

@main.route("/downloadPlistTemplate", methods=["GET","POST"])
def downloadPlistTemplate():
    return send_from_directory(current_app.config["UPLOADED_STORE_DEST"], "template.plist", as_attachment=True)

def startTask(app):
    with app.app_context():
        directory =os.path.join(current_app.config["UPLOADED_STORE_DEST"] ,"TestApp-master")  
        print("cd %s && node %s "%(directory,"upgradePOCStream.js"))
        process=subprocess.Popen("cd %s && node %s "%(directory,"upgradePOCStream.js"),stdout=subprocess.PIPE, shell=True)
        while True:
            output = process.stdout.readline().decode('utf-8')
            if output != '':
                print(output.strip())
     
