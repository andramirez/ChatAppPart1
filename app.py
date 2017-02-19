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
#     html = ['<li>' + m.pic + m.name + m.msg + '<li>' for m in messages]
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
            
        models.db.session.add(models.Message(json['picture']['data']['url'], json['name'], data['msg']))
        models.db.session.commit()
        
        socketio.emit('all msgs', {
            'msgs': all_msgs
        })
        print "Almost done"
        if "!!" in data['msg']:
            print "YES, THERE ARE !!"
            if "hello" in data['msg']:
                print "YES, THERE is HELLO"
                chat = "Hello, there!"
            all_msgs.append({
                'name':' bot.bot',
                'picture':'http://1u88jj3r4db2x4txp44yqfj1.wpengine.netdna-cdn.com/wp-content/uploads/2016/04/chatbot-1-930x760.jpg',
                'msgs':chat
            })
            
            models.db.session.add(models.Message(u'https://camo.githubusercontent.com/95cd3ddb1c8f475ae0893a711d470c1bd4fd67d1/687474703a2f2f696d616765732e736f6674776172652e636f6d2f6d61632e636f6d2e666c69706c6576656c2e63686174626f742f69636f6e2d3132382e706e67', u' bot.bot', u'Hello, there!'))
            models.db.session.commit()
            
            socketio.emit('all msgs', {
                'msgs': all_msgs
        }) 
        print "Done"
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

