import React, { Component } from "react";
import Image from "react-bootstrap/Image";
import CrossfadeImage from "react-crossfade-image";

class Environment extends Component {
  state = {
    environment: [[("", "", 0), ("", "", 0), ("", "", 0)]],
  };

  render() {
    return (
      <div className="environment">
        <CrossfadeImage src={`${this.props.imageSrc}?${this.props.imageHash}`} rounded />
      </div>
    );
  }
}

export default Environment;
