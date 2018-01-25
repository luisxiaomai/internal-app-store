from . import db

class Project(db.Model):
    __tableName_ = "Project"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    version = db.Column(db.String(64))
    description = db.Column(db.Text())
    android_jenkins_url = db.Column(db.String(64))
    ios_jenkins_url = db.Column(db.String(64))
    plist_name = db.Column(db.String(64))
    plist_url = db.Column(db.String(64))

    def __repr__(self):
        return "<Project %r>"%self.name
        