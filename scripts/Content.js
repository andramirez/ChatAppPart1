import * as React from 'react';
import { Button } from './Button';
import { Socket } from './Socket';

export class Content extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            'msgs': [],
        };
    }
    componentDidMount() {
      Socket.on('all msgs', (data) => {
          this.setState({
              'msgs': data['msgs']
          });
      })
  }
  render() {
    const style = {
      border:'.5px solid black', 
      textAlign:'left',
      padding:'2px',
      width: '495px',
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
    const image={
      width: 16, 
      height: 16
      
    }
    let msgs = this.state.msgs.map(
            (n, index) => <div key = {index} style={style} id="text1"><img style={image} src={n.picture}/><b>{n.name}:</b>{n.msgs}</div>
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
