import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import InstanceList from './components/InstanceList';
import "react-toggle/style.css"

// Routing
import { Route, Link, BrowserRouter as Router } from 'react-router-dom';

// Components
import Chat from './components/Chat';
import SHRDLUNavbar from './components/Navbar';


const routing = (
  <div>
    <SHRDLUNavbar />
    <Router>
      <Route exact path="/" component={Chat} />
      <Route path="/instances" component={InstanceList} />
    </Router>
  </div>
);

ReactDOM.render(routing,document.getElementById('root'));
