import flask_sqlalchemy
import app
import os

app.app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db = flask_sqlalchemy.SQLAlchemy(app.app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True) # key
    name = db.Column(db.String(120))
    pic = db.Column(db.String(300))
    msg = db.Column(db.String(120))
    
    def __init__(self, content):
        self.name = content['name']
        self.pic = content['picture']
        self.msg = content['msgs']
    
    def __repr__(self): 
        return '<Message text: %s %s %s>' % self.pic %self.name %self.msg