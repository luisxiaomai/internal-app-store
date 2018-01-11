from flask import render_template, send_from_directory
from . import main
import os

@main.route("/", methods=["GET","POST"])
def index():
    appList = [1,2,3]
    return render_template('index.html', appList=appList)

@main.route("/download/<filename>", methods=["GET","POST"])
def download(filename):
    directory =os.path.join(os.getcwd(),"store") 
    return send_from_directory(directory, filename, as_attachment=True)