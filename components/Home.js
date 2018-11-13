'use strict'

import React, {Component} from 'react';
import {Platform, Text, View, StyleSheet} from 'react-native';

export default class Home extends Component {

    render() {
        return(
            <Text style={styles.container}> Home Page </Text>
        );
    }

}

const styles = StyleSheet.create({
  container: {
    paddingTop: 100,
    paddingRight: 50,
    paddingLeft: 50
  },
});
