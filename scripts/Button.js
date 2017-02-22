import * as React from 'react';

import { Socket } from './Socket';

export class Button extends React.Component {
    
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
        });
        let auth = gapi.auth2.getAuthInstance();
        let user = auth.currentUser.get();
        if(user.isSignedIn()){
            Socket.emit('new msg',{
                    'google_user_token': user.getAuthResponse().id_token,
                    'msg': document.getElementById("msg").value,
                    'name': user['w3']['ig'],
                    'picture': user['w3']['Paa'],
            });
            
        }
        
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
