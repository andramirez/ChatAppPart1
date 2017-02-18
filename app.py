import os
import flask
import flask_socketio
import flask_sqlalchemy
import requests

app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)

import models

@app.route('/')
# def index():
#     messages = models.Message.query.all()
#     html = ['<li>' + m.text + '<li>' for m in messages]
#     return '<ul>' + ''.join(html) + '</ul>'
    
def hello():
    return flask.render_template('index.html')

@socketio.on('connect')
def on_connect():
    print 'Someone connected!'

@socketio.on('disconnect')
def on_disconnect():
    print 'Someone disconnected!'

all_msgs = []
@socketio.on('new msg')
def on_new_msg(data):
    print "Got an event for new number with data:", data
    if 'facebook_user_token' in data:
        response = requests.get('https://graph.facebook.com/v2.8/me?fields=id%2Cname%2Cpicture&access_token='+ data['facebook_user_token'])
        json=response.json()
        all_msgs.append({
            'name':" " + json['name'],
            'picture':json['picture']['data']['url'],
            'msgs':data['msg']
            })
            
        models.db.session.add(models.Message(json['name'] + data['msg'] + json['picture']['data']['url']))
        models.db.session.commit()
        
        socketio.emit('all msgs', {
            'msgs': all_msgs
        })
    else:
        print 'I MADE IT INTO GOOGLE';
        response = requests.get('https://www.googleapis.com/oauth2/v3/tokeninfo?id_token=' + data['google_user_token'])
        json=response.json()
        all_msgs.append({
            'name':" " + json['name'],
            'picture':json['picture'],
            'msgs':data['msg']
            })
        socketio.emit('all msgs', {
            'msgs': all_msgs
        })
        
if __name__ == '__main__': 
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )

