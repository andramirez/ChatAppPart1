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
      padding:'2px'
    };
    const AppStyle = {
      backgroundImage:'../images/bg.jpg'
    }
    let msgs = this.state.msgs.map(
            (n, index) => <div key = {index} style={style} id="text1"><img src={n.picture}/> {n.name}: {n.msgs}</div>
    );
    
    return (
      <div className="App" style={AppStyle}>
          <div id="live" className = "small-container">
            <h3>Please Sign In Using Google or Facebook</h3>
            <div className="g-signin2" data-onsuccess="onSignIn" data-theme="dark"></div>
          <div 
          className="fb-login-button" 
          data-max-rows="1" 
          data-size="medium" 
          data-show-faces="false" 
          data-auto-logout-link="true">
          </div>
        </div>
        <div id="msgBox">
          <h3>Welcome to the Chat Room</h3>
          <div id="chatbox">
            <div id="text">{ msgs }</div>
          </div>
          <Button/>
        </div>
      </div>
    );
  }
  
}
