import React, { Component } from 'react';
import axios from 'axios';

import ChatInput from './ChatInput';
import ChatMessageList from './ChatMessageList';

class Chat extends Component {
  state = {
    messages: [],
    name: 'Me'
  }

  // Send message to backend then print it to console
  sendMessage = (message) => {
    // add message to chat history
    this.addMessage(message);

    // send message to backend
    axios.post('http://0.0.0.0:5555/sentences', {
        sass: message.text
      })
      .then((res) => {
        // add response to history
        let response = {name: 'SHRDLU', text: res.data.sentences.sass};
        this.addMessage(response);
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
    const message = { name: this.state.name, text: messageString };
    this.sendMessage(message);
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
