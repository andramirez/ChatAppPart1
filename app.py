import os
import flask
import flask_socketio
import flask_sqlalchemy
import requests
import time
import random

app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)

import models

all_msgs = []
riddle = 0;
all_users = []
##current database print out
@app.route('/')

#prints database to the chatbox
# def index():
#     # messages = models.Message.query.all()
#     # html = ['<li>' + m.picture + m.name + m.message + '<li>' for m in messages]
#     # return '<ul>' + ''.join(html) + '</ul>'
    
#     recent = models.db.session.query(models.Message).order_by(models.Message.id.desc()).limit(100)
#     for row in recent.from_self().order_by(models.Message.id):
#             all_msgs.append({'picture':row.picture,'name':row.name,'message':row.message})
    
#     picture = [m['picture'] for m in all_msgs]
#     name = [m['name'] for m in all_msgs]
#     message = [m['message'] for m in all_msgs]
#     # html = ['<div id="text1"><img src=' + m['picture'] + '/><b>'+ m['name'] +':</b>'+ m['message'] +'</div>' for m in all_msgs]
#     return flask.render_template('index.html', pic = picture, nm=name, ms=message)

##template     
def hello():
    return flask.render_template('index.html')

##socket connection/ datbase
@socketio.on('connect')
def on_connect():
    print 'Someone connected!'

#socket disconnect
@socketio.on('disconnect')
def on_disconnect():
    print 'Someone disconnected!'


#bot messages    
def bot_msg(argument):
    if "hello" in argument.lower(): #returns a greeting
        return " Hello, there!"
    elif "riddle" in argument.lower(): #returns a riddle
        riddles = {
            1: "The more you take, the more you leave behind. What am I?",
            2: "I don't have eyes, but once I did see. Once I had thoughts, but now I'm white and empty.",
            3: "What belongs to you but others use it more than you do?"
        }
        riddle = random.randint(1, len(riddles))
        return riddles[riddle]
        
    elif "answer" in argument.lower(): #returns answer to riddle
        if(riddle == 0):
            return "You haven't received a riddle yet! <br/>To ask for a riddle, type: '!!riddle'"
        else:
            answers ={
                1: "Footsteps",
                2: "A Skull",
                3: "Your name"
            }
            return answers[riddle]
    elif "connected" in argument.lower(): #returns user connected message
        return " A user has connected! Name: "
    elif "about" in argument.lower(): # returns description
        return " Welcome to the Chat Room! Feel free to send messages to each other or to me!"
    elif "time" in argument.lower(): #returns current time
        return " The current time is: " + time.strftime("%I:%M:%S")
    elif "say" in argument.lower(): #returns message sent by user
        return argument.split("say")[1]
    elif "help" in argument.lower(): # returns list of commands
        return " Current Commands:<br/> !!hello: replies with a greeting<br/>!!about: gives description of chatroom<br/> !!help: returns known commands<br/> !!say <something>: has bot repeat message"
    else: #command wasn't recognied. Returns error message
        return " I don't recognize that command! Please type in '!!help' to receive a list of my commands"

@socketio.on('new user')
def on_new_user(data):
        ##Facebook login
    if 'facebook_user_token' in data:
        response = requests.get('https://graph.facebook.com/v2.8/me?fields=id%2Cname%2Cpicture&access_token='+ data['facebook_user_token'])
        json=response.json()
        count = len(all + 1)
        all_users.append({ ##retrieving facebook data
            'name':json['name'],
            'count': count
        })
        socketio.emit('all users', {
            'users': all_users
        })

## appending all aspects of message
@socketio.on('new msg')
def on_new_msg(data):
    ##Facebook login
    if 'facebook_user_token' in data:
        response = requests.get('https://graph.facebook.com/v2.8/me?fields=id%2Cname%2Cpicture&access_token='+ data['facebook_user_token'])
        json=response.json()
        all_msgs.append({ ##retrieving facebook data
            'name':" " + json['name'],
            'picture':json['picture']['data']['url'],
            'msgs':data['msg']
            })
        ##add data to the database    
        models.db.session.add(models.Message(json['picture']['data']['url'], json['name'], data['msg']))
        models.db.session.commit()
        
        socketio.emit('all msgs', {
            'msgs': all_msgs
        })
         ##checks if bot was referenced with !!
        if "!!" in data['msg']:
            bot = bot_msg(data['msg'])
            if "connected" in data['msg']:
                bot = bot + json['name']
            all_msgs.append({
            'name':" bot.bot",
            'picture':"https://camo.githubusercontent.com/95cd3ddb1c8f475ae0893a711d470c1bd4fd67d1/687474703a2f2f696d616765732e736f6674776172652e636f6d2f6d61632e636f6d2e666c69706c6576656c2e63686174626f742f69636f6e2d3132382e706e67",
            'msgs':bot
            })
            models.db.session.add(models.Message(u'https://camo.githubusercontent.com/95cd3ddb1c8f475ae0893a711d470c1bd4fd67d1/687474703a2f2f696d616765732e736f6674776172652e636f6d2f6d61632e636f6d2e666c69706c6576656c2e63686174626f742f69636f6e2d3132382e706e67', u' bot.bot', "u'"+bot+"'"))
            models.db.session.commit()
            
            socketio.emit('all msgs', {
                'msgs': all_msgs
        }) 
        #Google auth not implemented.. 
    # else:
    #     print 'I MADE IT INTO GOOGLE';
    #     response = requests.get('https://www.googleapis.com/oauth2/v3/tokeninfo?id_token=' + data['google_user_token'])
    #     json=response.json()
    #     all_msgs.append({
    #         'name':" " + json['name'],
    #         'picture':json['picture'],
    #         'msgs':data['msg']
    #         })
    #     socketio.emit('all msgs', {
    #         'msgs': all_msgs
    #     })
        
if __name__ == '__main__': 
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
)