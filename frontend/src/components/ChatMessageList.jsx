import React, { Component } from 'react';

import ChatMessage from './ChatMessage';

class ChatMessageList extends Component {

   constructor(props) {
    super(props);

  }
  render() {
    return this.props.messages.map((message, index) =>
          <ChatMessage
            key={index}
            message={message.message}
            name={"Me:"}
          />);
  }
}

export default ChatMessageList;
