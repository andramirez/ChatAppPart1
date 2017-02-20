import * as React from 'react';
import { Button } from './Button';
import { Button } from './Login';
import { Socket } from './Socket';

export class Content extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            'msgs': [],
        };
    }
    //msgs socket
    componentDidMount() {
      Socket.on('all msgs', (data) => {
          this.setState({
              'msgs': data['msgs']
          });
      })
      //users socket
      Socket.on('all users', (data) => {
          this.setState({
              'users': data['users']
          })
      })
  }
  render() {
    const style = {
      border:'.5px solid black', 
      textAlign:'left',
      padding:'2px',
      width: '895px',
      whitespace: 'nowrap',
      overflow: 'hidden',
      textoverflow: 'ellipsis'
    };
    const chat = {
      background: 'rgba(190, 190, 190, .75)'
    };
    const chatbox ={
      visibility:'hidden'
    }
     //goes inside log div
    let msgs = this.state.msgs.map(
            (n, index) => <div key = {index} style={style} id="text1"><img src={n.picture}/><b>{n.name}:</b>{n.msgs}</div>
    );
    
    //goes in users tag. List of users in the chat
    let users = this.state.users.map(
            (u, user) => <div key = {user} style={style} id="users"><b>{u.name}</b></div>
    );
    //goes in users tag. Is the count of how many users is in the chat
    let counts = this.state.users.map(
            (c, count) => <div key = {count} id="count"><b>{c.count}</b></div>
    );
    
    return (
      <div className="App">
          <div id="live" id = "small-container">
            <h3>Please Sign In Using Google or Facebook</h3>
            <Login/>          
          <div 
            className="g-signin2" 
            data-theme="dark">
          </div>
        </div>
        <div id="msgBox">
          <div id="welcome">Welcome to the Chat Room</div>
          <div id="users">Number of users: {counts}<br/>{users}</div>
          <div id="chatbox" style = {chat}>
            <div id="log">{msgs}</div> 
          </div>
        <Button/>
        </div>
      </div>
    );
  }
  
}