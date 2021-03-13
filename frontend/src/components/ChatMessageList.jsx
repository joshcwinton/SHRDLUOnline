import React, { Component } from 'react';

import ChatMessage from './ChatMessage';

class ChatMessageList extends Component {

  chatContainer = React.createRef();

   constructor(props) {
     super(props);
   }

  componentDidUpdate  = () => {
    this.scrollToMyRef();
  }
  scrollToMyRef = () => {
    const scroll = this.chatContainer.current.scrollHeight - this.chatContainer.current.clientHeight;

    this.chatContainer.current.scrollTo(0, scroll);
  };
  render() {
    return (
      <div ref={this.chatContainer} className="Chat">
      {this.props.messages.map((message, index) =>(
          <ChatMessage
            key={index}
            message={message.text}
            name={message.name}
          />))}
      </div>

    );
  }
}

export default ChatMessageList;
