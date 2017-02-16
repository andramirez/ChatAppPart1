import * as React from 'react';
import { Button } from './Button';
import { Socket } from './Socket';

export class Content extends React.Component {
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
