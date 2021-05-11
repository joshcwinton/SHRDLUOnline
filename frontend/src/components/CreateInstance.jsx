import React, { Component } from "react";
import { Form, Button, Container, Jumbotron } from "react-bootstrap";
import { useHistory } from "react-router-dom";
import axios from "axios";

import { getURI } from "../utils/config";

class CreateInstance extends Component {
  constructor(props) {
    super(props);
    this.state = {
      instanceName: "",
      creatorName: "",
      instanceSize: "",
    };

    this.handleInputChange = this.handleInputChange.bind(this);
  }

  handleInputChange(event) {
    const target = event.target;
    const value = target.value;
    const name = target.name;

    this.setState({
      [name]: value,
    });
  }

  handleSubmit = () => {
    console.log(getURI());
    axios
      .post(`${getURI()}/createinstance`, {
        instanceName: this.state.instanceName,
        creatorName: this.state.creatorName,
        instanceSize: this.state.instanceSize,
      })
      .then((res) => {
        console.log(res);
      })
      .catch((err) => {
        console.log(err);
      });

    // this.props.history.push(`/instances`);
  };

  render = () => {
    return (
      <Container>
        <h1>Create a new instance</h1>
        <Form onSubmit={this.handleSubmit}>
          <Form.Group controlId="formInstanceName">
            <Form.Label>Instance name</Form.Label>
            <Form.Control
              name="instanceName"
              type="text"
              value={this.state.instanceName}
              placeholder="Enter instance name"
              onChange={this.handleInputChange}
            />
          </Form.Group>

          <Form.Group controlId="formCreatorName">
            <Form.Label>Creator</Form.Label>
            <Form.Control
              name="creatorName"
              type="text"
              value={this.state.creatorName}
              placeholder="Enter your name"
              onChange={this.handleInputChange}
            />
          </Form.Group>

          <Form.Group controlId="formInstanceSize">
            <Form.Label>Instance size</Form.Label>
            <Form.Control
              name="instanceSize"
              type="number"
              value={this.instanceSize}
              placeholder="Enter instance size, e.g. 5 gives 5x5 square"
              onChange={this.handleInputChange}
            />
          </Form.Group>

          <Button variant="primary" type="submit">
            Submit
          </Button>
        </Form>
      </Container>
    );
  };
}

export default CreateInstance;
