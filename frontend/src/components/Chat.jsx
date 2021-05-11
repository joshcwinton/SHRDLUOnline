import React, { Component } from "react";
import axios from "axios";
import Toggle from "react-toggle";
import {
  Row,
  Col,
  ButtonGroup,
  Container,
  ToggleButton,
} from "react-bootstrap";

import ChatInput from "./ChatInput";
import ChatMessageList from "./ChatMessageList";
import Environment from "./Environment";

import { getURI } from "../utils/config";

class Chat extends Component {
  constructor(props) {
    super(props);
    let instanceName = props.match.params.instanceName;

    this.state = {
      messages: [],
      name: "Me",
      errors: [],
      imageSrc: `${getURI()}/environment_image`,
      imageHash: Date.now(),
      ml: false,
    };
  }

  // Send message to backend then print it to console
  sendMessage = (message) => {
    // add message to chat history
    this.addMessage(message);
    let errors = [];
    // send message to backend
    axios
      .post(`${getURI()}/${this.state.ml ? "ml" : ""}chat`, {
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
      .post(`${getURI()}/undo`)
      .then((res) => {
        // add response to chat history
        let userMessage = { name: "Me", text: res.data.Me };
        let response = { name: "SHRDLU", text: res.data.SHRDLU };
        this.addMessage(userMessage);
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

  clearBoard = () => {
    console.log("Clear Board");
    let errors = [];
    axios
      .post(`${getURI()}/clear`)
      .then((res) => {
        // add response to chat history
        let userMessage = { name: "Me", text: res.data.Me };
        let response = { name: "SHRDLU", text: res.data.SHRDLU };
        this.addMessage(userMessage);
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

  // TODO: This will likely involve a user param later on
  componentDidMount = () => {
    axios.get(`${getURI()}/messages`).then((res) => {
      let fetchedMessages = res.data.messages;
      this.setState({
        messages: fetchedMessages,
      });
    });
  };

  setChecked = (e) => {
    console.log(this.state.ml);
    if (this.state.ml == true) {
      this.setState((state) => {
        return { ml: false };
      });
    } else {
      this.setState((state) => {
        return { ml: true };
      });
    }
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
            <div>
              <button onClick={this.undoAction}>Undo</button>

              <button onClick={this.clearBoard}>Clear Board</button>

              <label>Machine Learning</label>
              <Toggle
                defaultChecked={this.state.ml}
                onChange={this.setChecked}
              />

              {this.state.errors.map((error, i) => (
                <p key={i} className="error">
                  {error}
                </p>
              ))}
            </div>
          </Col>
        </Row>
      </Container>
    );
  }
}

export default Chat;
