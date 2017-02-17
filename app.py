import os
import flask
import flask_socketio
import requests
# from oauth2client import client, crypt

app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)

@app.route('/')
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
    if data['facebook_user_token'] == "":
        print 'd'
        # try:
        #     idinfo = client.verify_id_token(data['google_user_token'], '985898840926-hgsdmkcas5969msavv6oe3tf4e651k5d.apps.googleusercontent.com')
        
        #     if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
        #         raise crypt.AppIdentityError("Wrong issuer.")
        # except crypt.AppIdentityError:
        #     # Invalid token
        #     print 'Invalid Token'
        # userid = idinfo['sub']
        # response = requests.get('https://www.googleapis.com/oauth2/v3/tokeninfo?id_token=' + userid)
    else:
        response = requests.get('https://graph.facebook.com/v2.8/me?fields=id%2Cname%2Cpicture&access_token='+ data['facebook_user_token'])
    json=response.json()
    all_msgs.append({
        'name':" " + json['name'],
        'picture':json['picture']['data']['url'],
        'msgs':data['msg']
        })
    socketio.emit('all msgs', {
        'msgs': all_msgs
    })

socketio.run(
    app,
    host=os.getenv('IP', '0.0.0.0'),
    port=int(os.getenv('PORT', 8080)),
    debug=True
)

