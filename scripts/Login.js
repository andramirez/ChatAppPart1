import * as React from 'react';

import { Socket } from './Socket';

export class Login extends React.Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.disableMe();
        this.clicked = false
        this.trigger = false;
    }
    
    handleSubmit(event) {
        event.preventDefault();
        if(this.disableMe())
        {
            this.clicked = true;
            FB.getLoginStatus((response) => {
                if (response.status == 'connected') {
                    Socket.emit('new msg', {
                        'facebook_user_token': response.authResponse.accessToken,
                        'msg': '!! connected' //My bot sees this and goes oh! and does botmsg = json['name'] + ' has entered the chatroom.'
                    });
                }
                else{
                    this.trigger = true;
                }
                
            });
            if(this.trigger == true)
            {
                let auth = gapi.auth2.getAuthInstance();
                let user = auth.currentUser.get();
                if (user.isSignedIn()){
                    Socket.emit('new msg', {
                        'login': 'Google', 
                        'name': user['w3']['ig'],
                        'picture': user['w3']['Paa'],
                        'msg': '!! connected' //My bot sees this and goes oh! and does botmsg = json['name'] + ' has entered the chatroom.'

                    });
                }
            }
            this.trigger = false;
        }
    }
    disableMe() {
        if (document.getElementById) {
            if (this.clicked == false) {
                return true;
            }
        } 
    }

            
    render() {
        return (
            <div>
                <form onSubmit={this.handleSubmit}>
                  <input type="submit" id="connect" value="Make Connection"></input>
                </form>
            </div>
        );
    }
}

