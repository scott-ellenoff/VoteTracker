'use strict'

import React, {Component} from 'react';
import {Platform, 
        Text,
        View,
        StyleSheet,
        TextInput} from 'react-native';

export default class Profile extends Component {
    static navigationOptions = {
        title: 'Profile',
    }

    render() {
        return(
            <View style={styles.container}>
            <Text> Profile Page </Text>
            </View>
        );
    }

}

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    paddingTop: 200,
    paddingRight: 50,
    paddingLeft: 50
  },
});
