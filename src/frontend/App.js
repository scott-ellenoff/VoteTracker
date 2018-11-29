'use strict'

import React, {Component} from 'react';

import Home from './components/Home.js';
import Main from './components/Main/Main.js';
import BillInfo from './components/Main/BillInfo';
import Profile from './components/Profile/Profile.js';
import Signup from './components/Signup/Signup.js';

import {
  createStackNavigator,
} from 'react-navigation'

const App = createStackNavigator(
  {
    Home: {screen: Home},
    Main: {screen: Main},
    Profile: {screen: Profile},
    BillInfo: {screen: BillInfo},
    Signup: {screen: Signup},
  }
);

export default App;
