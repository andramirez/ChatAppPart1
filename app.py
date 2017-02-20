import os
import flask
import flask_socketio
# import flask_sqlalchemy
import requests

app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)

# import models

all_messages = []

@app.route('/')
# def index():
#     recent = models.db.session.query(models.Message).order_by(models.Message.id.desc()).limit(100)
#     for row in recent.from_self().order_by(models.Message.id):
#   	    all_messages.append({'picture':row.picture,'name':row.name,'message':row.message})
#     return flask.render_template('index.html')
    
# ##template     
def hello():
    return flask.render_template('index.html')

@socketio.on('connect')
def on_connect():
    print 'Someone connected!'

#socket disconnect
@socketio.on('disconnect')
def on_disconnect():
    print 'Someone disconnected!'

#bot messages    
def bot_message(argument):
    if "hello" in argument:
        return "Hello, there!"
    if "about" in argument:
        return "Welcome to the Chat Room! Feel free to send messages to each other or to me!"
    if "help" in argument:
        return "Current Commands:</br> !!hello: replies with a greeting</br>!!about: gives description of chatroom</br> !!help: returns known commands</br !!say <something>: has bot repeat message"

## appending all aspects of message
@socketio.on('new message')
def on_new_msg(data):
    print "IN ON_NEW_MSG"
    ##Facebook login
    if 'facebook_user_token' in data:
        print "IN FACEBOOK"
        response = requests.get('https://graph.facebook.com/v2.8/me?fields=id%2Cname%2Cpicture&access_token='+ data['facebook_user_token'])
        json=response.json()
        all_messages.append({ ##retrieving facebook data
            'picture':json['picture']['data']['url'],
            'name':" " + json['name'],
            'messages':data['message']
            })
        ##add data to the database    
        # models.db.session.add(models.Message(json['picture']['data']['url'], json['name'], data['message']))
        # models.db.session.commit()
        
        socketio.emit('all messages', {
            'messages': all_messages
        })
        
        # if "!!" in data['message']:
        #     bot = bot_message(data['message'])
        #     all_messages.append({
        #     'picture':"https://camo.githubusercontent.com/95cd3ddb1c8f475ae0893a711d470c1bd4fd67d1/687474703a2f2f696d616765732e736f6674776172652e636f6d2f6d61632e636f6d2e666c69706c6576656c2e63686174626f742f69636f6e2d3132382e706e67",
        #     'name':" bot.bot",
        #     'messages':bot
        #     })
        #     # models.db.session.add(models.Message(u'https://camo.githubusercontent.com/95cd3ddb1c8f475ae0893a711d470c1bd4fd67d1/687474703a2f2f696d616765732e736f6674776172652e636f6d2f6d61632e636f6d2e666c69706c6576656c2e63686174626f742f69636f6e2d3132382e706e67', u' bot.bot', "u'"+bot+"'"))
        #     # models.db.session.commit()
            
        #     socketio.emit('all messages', {
        #         'messages': all_messages
        # }) 
        
    # else:
    #     response = requests.get('https://www.googleapis.com/oauth2/v3/tokeninfo?id_token=' + data['google_user_token'])
    #     json=response.json()
    #     all_messages.append({
    #         'name':" " + json['name'],
    #         'picture':json['picture'],
    #         'messages':data['message']
    #         })
    #     socketio.emit('all messages', {
    #         'messages': all_messages
    #     })
        
if __name__ == '__main__': 
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )

