from . import db

class Project(db.Model):
    __tableName_ = "Project"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    version = db.Column(db.String(64), unique=True)
    description = db.Column(db.Text())
    jenkins_url = db.Column(db.String(64))

    def __repr__(self):
        return "<Project %r>"%self.name
