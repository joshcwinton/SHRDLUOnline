import React, { Component } from "react";
import axios from "axios";

import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

import ChatInput from "./ChatInput";
import ChatMessageList from "./ChatMessageList";
import Environment from "./Environment";

import { getURI } from "../utils/config";

class Chat extends Component {
  state = {
    messages: [],
    name: "Me",
    errors: [],
    imageSrc: `${getURI()}/environment_image`,
    imageHash: Date.now(),
  };

  // Send message to backend then print it to console
  sendMessage = (message) => {
    // add message to chat history
    this.addMessage(message);
    let errors = [];
    // send message to backend
    axios
      .post(`${getURI()}/chat`, {
        user: message.text,
      })
      .then((res) => {
        // add response to history
        let response = { name: "SHRDLU", text: res.data.SHRDLU };
        this.addMessage(response);
        this.updateEnvironment();
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

  updateEnvironment = () => {
    this.setState({
      imageSrc: `${getURI()}/environment_image`,
      imageHash: Date.now(),
    });
  };

  undoAction = () => {
    console.log("Undo Action");
    let errors = [];
    axios
      .post("https:shrdluonline-backend.herokuapp.com/undo")
      .then((res) => {
        // add response to chat history
        let response = { name: "SHRDLU", text: res.data.SHRDLU };
        this.addMessage(response);
        this.updateEnvironment();
      })
      .catch((err) => {
        console.log(err);
        errors.push(err.message);
      })
      .finally(() => {
        this.setState({ errors: errors });
      });
  }

  clearBoard  = () => {
    console.log("Clear Board");
    let errors = [];
    axios
      .post("https:shrdluonline-backend.herokuapp.com/clear")
      .then((res) => {
        // add response to chat history
        let response = { name: "SHRDLU", text: res.data.SHRDLU };
        this.addMessage(response);
        this.updateEnvironment();
      })
      .catch((err) => {
        console.log(err);
        errors.push(err.message);
      })
      .finally(() => {
        this.setState({ errors: errors });
      });
  }


  // TODO: This will likely involve a user param later on
  componentDidMount = () => {
    axios.get(`${getURI()}/messages`).then((res) => {
      let fetchedMessages = res.data.messages;
      this.setState({
        messages: fetchedMessages,
      });
    });
  };

  render() {
    return (
      <Container fluid="sm">
        <Row>
          <Col>
            <Environment
              imageSrc={this.state.imageSrc}
              imageHash={this.state.imageHash}
            />
          </Col>
          <Col>
            <ChatMessageList messages={this.state.messages} />
            <ChatInput
              onSubmitMessage={(messageString) =>
                this.submitMessage(messageString)
              }
            />
            <button onClick={this.undoAction}>
              Undo
            </button>

            <button onClick={this.clearBoard}>
              Clear Board
            </button>

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
