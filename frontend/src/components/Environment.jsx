import React, { Component } from "react";
import Image from "react-bootstrap/Image";

class Environment extends Component {
  state = {
    environment: [[("", "", 0), ("", "", 0), ("", "", 0)]],
  };

  render() {
    return (
      <div className="environment">
        <Image src="shrdlu-placeholder.jpg" rounded />
      </div>
    );
  }
}

export default Environment;
