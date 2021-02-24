import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';

// Routing
import { Route, Link, BrowserRouter as Router } from 'react-router-dom';

// Components
import Chat from './components/Chat';

const routing = (
  <Router>
    <Route exact path="/" component={Chat} />
  </Router>
);

ReactDOM.render(routing,document.getElementById('root'));
