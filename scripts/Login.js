import * as React from 'react';

import { Socket } from './Socket';

export class Login extends React.Component {
    constructor(props) {
        super(props);
        // this.handleSubmit = this.handleSubmit.bind(this);
        this.disableMe();
        this.clicked = false
    }
    loadPage(){
        FB.getLoginStatus((response) => {
                if (response.status == 'connected') {
                    Socket.emit('new msg', {
                        'facebook_user_token': response.authResponse.accessToken,
                        'msg': '!! connected' //My bot sees this and goes oh! and does botmsg = json['name'] + ' has entered the chatroom.'
                    });
                }
                else {
                    let auth = gapi.auth2.getAuthInstance();
                    let user = auth.currentUser.get();
                    if(user.isSignedIn()){
                        Socket.emit('new msg',{
                            'google_user_token': user.getAuthResponse().id_token,
                            'msg': '!! connected' //My bot sees this and goes oh! and does botmsg = json['name'] + ' has entered the chatroom.'
                        });
                        
                    }
                    
                }
            });
    }
    // handleSubmit(event) {
    //     event.preventDefault();
    //     if(this.disableMe())
    //     {
    //         this.clicked = true;
    //         FB.getLoginStatus((response) => {
    //             if (response.status == 'connected') {
    //                 Socket.emit('new msg', {
    //                     'facebook_user_token': response.authResponse.accessToken,
    //                     'msg': '!! connected' //My bot sees this and goes oh! and does botmsg = json['name'] + ' has entered the chatroom.'
    //                 });
    //             }
    //             else {
    //                 let auth = gapi.auth2.getAuthInstance();
    //                 let user = auth.currentUser.get();
    //                 if(user.isSignedIn()){
    //                     Socket.emit('new msg',{
    //                         'google_user_token': user.getAuthResponse().id_token,
    //                         'msg': '!! connected' //My bot sees this and goes oh! and does botmsg = json['name'] + ' has entered the chatroom.'
    //                     });
                        
    //                 }
                    
    //             }
    //         });
    //     }
    // }
    disableMe() {
        if (document.getElementById) {
            if (this.clicked == false) {
                return true;
            }
        } 
    }
            //     FB.logout(function(response) {
            //   // user is now logged out
            //         Socket.emit('new msg', {
            //             'facebook_user_token': response.authResponse.accessToken,
            //             'msg': '!! disconnected' //My bot sees this and goes oh! and does botmsg = json['name'] + ' has entered the chatroom.'
            //         });
            // });
    
    render() {
        return (
            <div>
                <div
                    className="fb-login-button"
                    data-max-rows="1"
                    data-size="medium"
                    data-show-faces="false"
                    data-auto-logout-link="true">
                </div>
                <div 
                    className="g-signin2" 
                    data-theme="dark">
                </div>
                <form onLoad="loadPage()">
                  <input type="submit" id="connect" value="Make Connection"></input>
                </form>
            </div>
        );
    }
}

