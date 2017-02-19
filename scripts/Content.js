import * as React from 'react';
import { Button } from './Button';
import { Socket } from './Socket';

export class Content extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            'messages': [],
        };
    }
    componentDidMount() {
      Socket.on('all messages', (data) => {
          this.setState({
              'messages': data['messages']
          });
      })
  }
  render() {
    const style = {
      border:'.5px solid black', 
      textAlign:'left',
      padding:'2px',
      width: '695px',
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

    let messages = this.state.messages.map(
            (n, index) => <div key = {index} style={style} id="text1"><img src={n.picture}/><b>{n.name}:</b>{n.messages}</div>
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
          data-auto-logout-link="true"
          >
          </div>            
          <div 
            className="g-signin2" 
            data-theme="dark">
          </div>
        </div>
        <div id="msgBox">
          <div id="welcome">Welcome to the Chat Room</div>
          <div id="chatbox" style={chat}>
            <div id="text">{ msgs }</div>
          </div>
          <Button/>
        </div>
      </div>
    );
  }
  
}
