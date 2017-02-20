import flask_sqlalchemy
import app
import os

app.app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

db = flask_sqlalchemy.SQLAlchemy(app.app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True) # key
    picture = db.Column(db.String(300))
    name = db.Column(db.String(500))
    message = db.Column(db.String(500))
    
    def __init__(self, p,n,m):
        self.pic = p
        self.name = n
        self.msg = m
    
    def __repr__(self): 
        return '<Message text: %s %s %s>' % self.pic %self.name %self.msg