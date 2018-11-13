'use strict'

import React, {Component} from 'react';
import {Platform, Text, View, StyleSheet} from 'react-native';

export default class Profile extends Component {
    static navigationOptions = {
        title: 'Profile Screen',
    }

    render() {
        return(
            <Text style={styles.container}> Profile Page </Text>
        );
    }

}

const styles = StyleSheet.create({
  container: {
    paddingTop: 200,
    paddingRight: 50,
    paddingLeft: 50
  },
});
