import React, { Component } from "react";
import { Link } from "react-router-dom";
import { Container, Table } from "react-bootstrap";
import axios from "axios";

import { getURI } from "../utils/config";
class InstanceList extends Component {
  state = {
    instances: [],
  };

  componentDidMount = () => {
    axios.get(`${getURI()}/instances`).then((res) => {
      let fetchedInstances = res.data.instances;
      this.setState({
        instances: fetchedInstances,
      });
    });
  };

  render() {
    return (
      <Container>
        <h1>Instances</h1>
        <Table striped bordered hover>
          <thead>
            <tr>
              <th>Name</th>
              <th>Creator</th>
              <th>Size</th>
            </tr>
          </thead>
          <tbody>
            {this.state.instances.map((instance) => {
              let id = instance[0];
              let name = instance[1];
              let creator = instance[2];
              let size = instance[3];
              return (
                <tr key={name}>
                  <td>
                    <Link to={`/instance/${id}`}>{name}</Link>
                  </td>
                  <td>{creator}</td>
                  <td>
                    {size} x {size}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </Table>
      </Container>
    );
  }
}

export default InstanceList;
