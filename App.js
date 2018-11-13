'use strict'

import React, {Component} from 'react';
import {Platform, Text, View} from 'react-native';

import Home from './components/Home.js'
import Main from './components/Main.js'
import Profile from './components/Profile.js'

import {
    createStackNavigator,
} from 'react-navigation'

const App = createStackNavigator(
    {
        Home: {screen: Home},
        Main: {screen: Main},
        Profile: {screen: Profile}
    }
);

export default App;
