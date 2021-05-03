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
              <th>Last Updated</th>
            </tr>
          </thead>
          <tbody>
            {this.state.instances.map((instance) => {
              return (
                <tr key={instance.name}>
                  <td>
                    <Link to={instance.url}>{instance.name}</Link>
                  </td>
                  <td>{instance.creator}</td>
                  <td>
                    {instance.size} x {instance.size}
                  </td>
                  <td>{instance.lastUpdated}</td>
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
