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
all_users = [] #-NEW
global riddle
riddle = 0;
##current database print out
@app.route('/')

#prints database to the chatbox
def index():
    recent = models.db.session.query(models.Message).order_by(models.Message.id.desc()).limit(200)
    for row in recent.from_self().order_by(models.Message.id):
            all_msgs.append({'picture':row.picture,'name':row.name,'msgs':row.message})
    return flask.render_template('index.html')


##socket connection/ datbase
@socketio.on('connect')
def on_connect():
    print 'Someone connected'

#socket disconnect
@socketio.on('disconnect')
def on_disconnect():
    print 'Someone disconnected!'

#bot messages    
def bot_msg(argument):
    if "hello" in argument.lower(): #returns a greeting
        return " Hello, there! Meow"
    elif "riddle" in argument.lower(): #returns a riddle
        riddles = {
            1: "The more you take, the more you leave behind. What am I? Type '!!answer' for the answer",
            2: "I don't have eyes, but once I did see. Once I had thoughts, but now I'm white and empty. Type '!!answer' for the answer",
            3: "What belongs to you but others use it more than you do? Type '!!answer' for the answer",
            4: "What is harder to catch the faster you run? Type '!!answer' for the answer",
            5: "You will always find me in the past. I can be created in the present, But the future can never taint me. What am I? Type '!!answer' for the answer",
            6: "An old man wanted to leave all of his money to one of his three sons, but he didn't know which one he should give it to. He gave each of them a few coins and told them to buy something that would be able to fill their living room. The first man bought straw, but there was not enough to fill the room. The second bought some sticks, but they still did not fill the room. The third man bought two things that filled the room, so he obtained his father's fortune. What were the two things that the man bought? Type '!!answer' for the answer",
            7: "What has a head, a tail, is brown, and has no legs? Type '!!answer' for the answer",
            8: "What begins with T, ends with T and has T in it? Type '!!answer' for the answer",
            9: "Wednesday, Tom and Joe went to a restaurant and ate dinner. When they were done they paid for the food and left. But Tom and Joe didn't pay for the food. Who did? Type '!!answer' for the answer",
            10: "What is big and yellow and comes in the morning, to brighten mom's day? Type '!!answer' for the answer"
        }
        riddle = random.randint(1, len(riddles))
        return riddles[riddle]
        
    elif "answer" in argument.lower(): #returns answer to riddle
        print riddle #might cause bug
        if(riddle == 0):
            return "You haven't received a riddle yet! <br>To ask for a riddle, type: '!!riddle'"
        else:
            index = riddle
            riddle = 0
            answers ={
                1: "Footsteps",
                2: "A Skull",
                3: "Your name",
                4: "Your breath",
                5: "History",
                6: "The wise son bought a candle and a box of matches. After lighting the candle, the light filled the entire room.",
                7: "A penny",
                8: "A teapot",
                9: "Wednesday (the name of the third person in the group, not the day)",
                10: "A School Bus"
            }
            return answers[index]
    elif "connected" in argument.lower(): #returns user connected message
        return " A user has connected! Name: "
    elif "about" in argument.lower(): # returns description
        return " Welcome to the Chat Room! Feel free to send messages to each other or to me! Meow"
    elif "time" in argument.lower(): #returns current time
        return " The current time is: " + time.strftime("%I:%M:%S") + " Meow"
    elif "say" in argument.lower(): #returns message sent by user
        return argument.split("say")[1] + ". I mean.... meow.."
    elif "help" in argument.lower(): # returns list of commands
        return " Current Commands: <br> \
        !!hello: I will greet you <br> \
        !!about: I'll tell you about the cat room <br> \
        !!help: I will tell you known commands <br> \
        !!say <something>: has bot repeat message <br> \
        !!riddle: I will ask you a riddle <br> \
        !!answer: I will answer the riddle. Only after you've asked, though <br> \
        !!time: I will tell you the current time"
    elif "welcomeMessage" in argument():
        return " Welcome to the Catroom. Please make sure to sign in"
    elif "disconnected" in argument():
        return " A user has disconnected! Name: "
    else: #command wasn't recognied. Returns error message
        return " I don't recognize that command! Please type in '!!help' to receive a list of my commands. Meow"
        
    
def bot_send(msg):
    bot = bot_msg(msg)
    all_msgs.append({
    'name':" cat.bot",
    'picture':"https://f4.bcbits.com/img/a2219945996_16.jpg",
    'msgs':bot
    })
    models.db.session.add(models.Message(u'https://f4.bcbits.com/img/a2219945996_16.jpg', 'cat.bot', bot))
    models.db.session.commit()
    
    socketio.emit('all msgs', {
        'msgs': all_msgs
    }) 
    # #user list -NEW
    if "cat.bot" not in all_users:
        all_users.append({
        'users': "cat.bot"
        })
        socketio.emit('all users', {
            'users': all_users
        })

## appending all aspects of message
@socketio.on('new msg')
def on_new_msg(data):
    if "!! welcomeMessage" in data['msg']:
            bot = bot_msg(data['msg'])
            all_msgs.append({
            'name':" cat.bot",
            'picture':"https://f4.bcbits.com/img/a2219945996_16.jpg",
            'msgs':bot
            })
            models.db.session.add(models.Message(u'https://f4.bcbits.com/img/a2219945996_16.jpg', 'cat.bot', bot))
            models.db.session.commit()
            
            #user list -NEW
            if "cat.bot" not in all_users:
                all_users.append({
                'users': "cat.bot"
                })
                socketio.emit('all users', {
                    'users': all_users
                })
            
    elif 'facebook_user_token' in data:
        if "!! connected" in data['msg'] or "!! disconnected" in data['msg']:
            response = requests.get('https://graph.facebook.com/v2.8/me?fields=id%2Cname%2Cpicture&access_token='+ data['facebook_user_token'])
            json=response.json()
            bot = bot_msg(data['msg'])
            bot = bot + json['name']
            all_msgs.append({
            'name':" cat.bot",
            'picture':"https://f4.bcbits.com/img/a2219945996_16.jpg",
            'msgs':bot
            })
            models.db.session.add(models.Message(u'https://f4.bcbits.com/img/a2219945996_16.jpg', 'cat.bot', bot))
            models.db.session.commit()
            
            socketio.emit('all msgs', {
                'msgs': all_msgs
            }) 
            ##emits for user list
            #user list -NEW
            if "cat.bot" not in all_users:
                 all_users.append({
                    'users': "cat.bot"
                })
            if json['name'] not in all_users:
                all_users.append({
                    'users': json['name']
                })
                socketio.emit('all users', {
                    'users': all_users
                })

            
        elif "login" in data:
            all_msgs.append({ ##retrieving facebook data
                'name': data['name'],
                'picture':data['picture'],
                'msgs':data['msg']
                })
            ##add data to the database    
            models.db.session.add(models.Message(data['picture'], data['name'], data['msg']))
            models.db.session.commit()
            
            socketio.emit('all msgs', {
                'msgs': all_msgs
            })
             ##checks if bot was referenced with !!
            if "!!" in data['msg']:
                bot = bot_msg(data['msg'])
                all_msgs.append({
                'name':" cat.bot",
                'picture':"https://f4.bcbits.com/img/a2219945996_16.jpg",
                'msgs':bot
                })
                models.db.session.add(models.Message(u'https://f4.bcbits.com/img/a2219945996_16.jpg', 'bot.bot', bot))
                models.db.session.commit()
                
                socketio.emit('all msgs', {
                    'msgs': all_msgs
                }) 
        
    else:
        if "!! connected" in data['msg'] or "!! disconnected" in data['msg']:
            response = requests.get('https://www.googleapis.com/oauth2/v3/tokeninfo?id_token=' + data['google_user_token'])
            json=response.json()
            bot = bot_msg(data['msg'])
            bot = bot + data['name']
            all_msgs.append({
            'name':" cat.bot",
            'picture':"https://f4.bcbits.com/img/a2219945996_16.jpg",
            'msgs':bot
            })
            models.db.session.add(models.Message(u'https://f4.bcbits.com/img/a2219945996_16.jpg', 'cat.bot', bot))
            models.db.session.commit()
            
            socketio.emit('all msgs', {
                'msgs': all_msgs
            }) 
    
            ##emits for user list
            #user list -NEW
            if "cat.bot" not in all_users:
                 all_users.append({
                    'users': "cat.bot"
                })
            if json['name'] not in all_users:
                all_users.append({
                    'users': json['name']
                })
                socketio.emit('all users', {
                    'users': all_users
                })
            
            
        else:
            response = requests.get('https://www.googleapis.com/oauth2/v3/tokeninfo?id_token=' + data['google_user_token'])
            json=response.json()
            all_msgs.append({
                'name':" " + json['name'],
                'picture':data['picture'],
                'msgs':data['name']
                })
            socketio.emit('all msgs', {
                'msgs': all_msgs
            })
            
            if "!!" in data['msg']:
                bot_send(data['msg'])
        
if __name__ == '__main__': 
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
)