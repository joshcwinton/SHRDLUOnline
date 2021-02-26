import React, { Component } from 'react';
import axios from 'axios';

import ChatInput from './ChatInput';
import ChatMessageList from './ChatMessageList';

class Chat extends Component {
  state = {
    messages: [],
  }

  // Send message to backend then print it to console
  sendMessage = (message) => {
    axios.post('localhost:8080/sentences', {
        message: message
      })
      .then((res) => {
        console.log(res);
      })
      .catch((err) => {
        console.log(err);
      });
  }

  addMessage = (message) => {
    this.setState(state => ({ messages: [ ...state.messages, message] }));
  }

  submitMessage = messageString => {
    // on submitting the ChatInput form, send the message, add it to the list and reset the input
    const message = { name: this.state.name, message: messageString };
    this.addMessage(message);
  }

  render() {
    return (
      <div>
        <ChatInput
          onSubmitMessage={messageString => this.submitMessage(messageString)}
        />
        <ChatMessageList messages={this.state.messages}/>
      </div>
    );
  }
}

export default Chat;
