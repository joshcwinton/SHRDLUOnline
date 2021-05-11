import React, { Component } from "react";
import { Form } from "react-bootstrap";

class CreateInstance extends Component {
  render = () => {
    return (
      <Form>
        <Form.Group>
          <Form.Label>Instance name</Form.Label>
          <Form.Control placeholder="Enter instance name" />
        </Form.Group>
        <Form.Group>
          <Form.Label>Creator</Form.Label>
          <Form.Control placeholder="Enter your name" />
        </Form.Group>
        <Form.Group>
          <Form.Label>Instance size</Form.Label>
          <Form.Control placeholder="" />
        </Form.Group>
      </Form>
    );
  };
}

export default CreateInstance;
