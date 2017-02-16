import React, { Component } from 'react';
import { Socket } from './Socket';
import { Button } from './Button';
import './App.css';

class App extends Component {
  componentDidMount() {
        Socket.on('all numbers', (data) => {
            this.setState({
                'msgs': data['numbers']
            });
        })
    }
  render() {
    return (
      <div className="App">
        <div id="msgBox">
          <div id="chatbox">
            <div id="text"></div>
          </div>
          <textarea id="msg" rows="4" cols="50" placeholder="Please insert text"></textarea> 
          <button id="b1">Submit</button>
        </div>
      </div>
    );
  }
}

export default App;
