import React, { Component } from "react";
import axios from "axios";

import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

import ChatInput from "./ChatInput";
import ChatMessageList from "./ChatMessageList";
import Environment from "./Environment";
import SampleCommands from "./SampleCommands";

class Chat extends Component {
  state = {
    messages: [],
    name: "Me",
    errors: [],
  };

  // Send message to backend then print it to console
  sendMessage = (message) => {
    // add message to chat history
    this.addMessage(message);
    let errors = [];
    // send message to backend
    axios
      .post("http://0.0.0.0:5555/chat", {
        user: message.text,
      })
      .then((res) => {
        // add response to history
        let response = { name: "SHRDLU", text: res.data.SHRDLU };
        this.addMessage(response);
      })
      .catch((err) => {
        console.log(err);
        errors.push(err.message);
      })
      .finally(() => {
        this.setState({ errors: errors });
      });
  };

  addMessage = (message) => {
    this.setState((state) => ({ messages: [...state.messages, message] }));
  };

  submitMessage = (messageString) => {
    // on submitting the ChatInput form, send the message, add it to the list and reset the input
    let errors = [];
    if (messageString === "") {
      console.log("Blank message is not valid!");
      errors.push("Blank message is not valid!");
    } else {
      const message = { name: this.state.name, text: messageString };
      this.sendMessage(message);
    }
    this.setState({ errors: errors });
  };

  render() {
    return (
      <Container fluid="sm">
        <SampleCommands />
        <Row>
          <Col>
            <Environment />
          </Col>
          <Col>
            <ChatMessageList messages={this.state.messages} />
            <ChatInput
              onSubmitMessage={(messageString) =>
                this.submitMessage(messageString)
              }
            />
            {this.state.errors.map((error, i) => (
              <p key={i} className="error">
                {error}
              </p>
            ))}
          </Col>
        </Row>
      </Container>
    );
  }
}

export default Chat;
