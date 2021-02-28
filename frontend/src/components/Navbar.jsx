import React, { Component } from "react";

import Navbar from "react-bootstrap/Navbar";
import Nav from "react-bootstrap/Nav";

class SHRDLUNavbar extends Component {
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
          </Nav>
        </Navbar>
      </div>
    );
  }
}
export default SHRDLUNavbar;
