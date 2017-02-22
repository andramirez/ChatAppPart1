import * as React from 'react';
import { Button } from './Button';
import { Socket } from './Socket';
import { Login } from './Login';

export class Content extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            'msgs': [],
             'users':[]
        };
    }
    
    //msgs socket
    componentDidMount() {
      Socket.on('all msgs', (data) => {
          this.setState({
              'msgs': data['msgs']
          });
      })
      //NEW
      Socket.on('all users', (data) => {
          this.setState({
              'users': data['users']
          });
      })
  }
    
  render() {
    
    const style = {
      border:'.5px solid black', 
      textAlign:'left',
      padding:'2px',
      width: '840px',
      whitespace: 'nowrap',
      overflow: 'hidden',
      textoverflow: 'ellipsis'
    };
    const chat = {
      background: 'rgba(190, 190, 190, .75)'
    };
     //goes inside log div
    let msgs = this.state.msgs.map(
            (n, index) => <div key = {index} style={style} id="text1"><img src={n.picture}/><b>{n.name}:</b>{n.msgs}</div>
    );
    //NEW
    let users = this.state.users.map(
            (n, index) => <li key = {index}  id="text2">{n.users}</li>
    );
    
    
    return (
      <div className="App">
          <div id="live" id = "small-container">
            <h3>Please Sign In Using Google or Facebook</h3>
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
          </div>
        <div id="msgBox">
          <div id="welcome">Welcome to the Cat Room</div>
          <div id="chatbox" style = {chat}>
            <div id="log">{msgs}</div> 
            <div id="userList"><ul>{users}</ul></div>
          </div>
        <Button/>
        </div>
      </div>
    );
  }
  
}