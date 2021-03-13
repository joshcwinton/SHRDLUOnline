import React, {Component} from 'react';
import Alert from 'react-bootstrap/Alert';
import Container from 'react-bootstrap/Container';

class SampleCommands extends Component{

  constructor(props){
    super();
    this.state = {show:props.show};

  }


  componentDidUpdate = (prevProps, prevState) => {

    if(prevProps != this.props){
      this.setState({show:this.props.show});
    }

  }

  render(){
    if(this.state.show){
      return (
        <Container fluid>
          <Alert variant="primary">
            <Alert.Heading>Try out these commands:</Alert.Heading>
            <ul>
              <li>"Add the red cube 2 2"</li>
              <li>"Add the pyramid"</li>
              <li>"Add the green"</li>
            </ul>
          </Alert>
        </Container>
      );
    }
    return (<div></div>);
  };
}

export default SampleCommands;
