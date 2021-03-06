import * as React from 'react';

import { Socket } from './Socket';

export class Button extends React.Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.trigger = false;
    }
    
    handleSubmit(event) {
        event.preventDefault();
        FB.getLoginStatus((response)=>{
            if(response.status=='connected'){
                Socket.emit('new msg',{
                    'facebook_user_token':
                    response.authResponse.accessToken,
                    'msg': document.getElementById("msg").value
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
                    'msg': document.getElementById("msg").value
                });
            }
        }
        this.trigger = false;
        
        document.getElementById("msg").value = "";
    }
    render() {

        return (
            <form onSubmit={this.handleSubmit}>
                <textarea id="msg" rows="4" cols="50" placeholder="Please insert text"></textarea> 
                <button id="b1">Send</button>
            </form>
        );
    }
}
