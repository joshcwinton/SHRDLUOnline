import React, { Component } from "react";

import Navbar from "react-bootstrap/Navbar";
import Nav from "react-bootstrap/Nav";
import SampleCommands from "./SampleCommands";

class SHRDLUNavbar extends Component {
  state = {
    show: false
  }

  handleClick = (e) =>{
    this.setState({show:!this.state.show});
  }

  render() {
    return (
      <div>
        <Navbar bg="dark" variant="dark">
          <Navbar.Brand href="#home">
            <img
              alt=""
              src="/logo.svg"
              width="30"
              height="30"
              className="d-inline-block align-top"
            />{" "}
            SHRDLU Online
          </Navbar.Brand>
          <Nav className="mr-auto">
            <Nav.Link href="/">Chat</Nav.Link>
            <Nav.Link href="/">Explore</Nav.Link>
            <Nav.Link href="/">Login</Nav.Link>
            <Nav.Link onClick={this.handleClick}> Toggle Help</Nav.Link>
          </Nav>
        </Navbar>
        <SampleCommands show={this.state.show} />
      </div>
    );
  }
}
export default SHRDLUNavbar;
