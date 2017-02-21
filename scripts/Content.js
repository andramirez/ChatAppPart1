import * as React from 'react';
import { Button } from './Button';
import { Login } from './Login';
import { Socket } from './Socket';

export class Content extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            'msgs': [],
        };
        //NEW
        this.state = {
          'users':[]
        }
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
            (n, index) => <li key = {index} style={style} id="text2">n.users</li>
    );
    
    
    return (
      <div className="App">
          <div id="live" id = "small-container">
            <h3>Please Sign In Using Google or Facebook</h3>
            <Login/>          
        </div>
        <div id="msgBox">
          <div id="welcome">Welcome to the Cat Rooms</div>
          <div id="chatbox" style = {chat}>
            <div id="log">{msgs}</div> 
          </div>
          <div id="userList"><ul>{users}</ul></div>
        <Button/>
        </div>
      </div>
    );
  }
  
}