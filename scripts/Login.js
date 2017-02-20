import * as React from 'react';

import { Socket } from './Socket';

export class Login extends React.Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
    }
    handleSubmit(event) {
        event.preventDefault();
        FB.getLoginStatus((response) => {
            if (response.status == 'connected') {
                Socket.emit('new msg', {
                    'facebook_user_token': response.authResponse.accessToken,
                    'msg': '!! connected' //My bot sees this and goes oh! and does botmsg = json['name'] + ' has entered the chatroom.'
                });
                Socket.emit('new user', {
                    'facebook_user_token': response.authResponse.accessToken,
                });
            }
        });
    }
    render() {
        return (
            <div>
                <div>
                    className="fb-login-button"
                    data-max-rows="1"
                    data-size="medium"
                    data-show-faces="false"
                    data-auto-logout-link="true"
                </div>
                <form onSubmit={this.handleSubmit}>
                  <input type="submit" value="Start App"></input>
                </form>
            </div>
        );
    }
}

