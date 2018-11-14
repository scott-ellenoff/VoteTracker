'use strict'

import React, {Component} from 'react';

import Home from './components/Home.js'
import Main from './components/Main/Main.js'
import Profile from './components/Profile/Profile.js'
import SelectLegislators from './components/Profile/selectLegislators';
import {
  createStackNavigator,
} from 'react-navigation'

const App = createStackNavigator(
  {
    Home: {screen: Home},
    Main: {screen: Main},
    Profile: {screen: Profile},
    SelectLegislators: {screen: SelectLegislators}
  }
);

export default App;
