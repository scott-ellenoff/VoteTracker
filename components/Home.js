'use strict'

import React, {Component} from 'react';
import {Platform, Text, View, StyleSheet, Button} from 'react-native';

export default class Home extends Component {
    static navigationOptions = {
        title: 'Home Screen',
    }

    render() {
        const {navigate} = this.props.navigation
        return(
            <View style={styles.container}>
                <Text> Home Page </Text>
                <Button
                    title="Go to Main Screen"
                    onPress={() => navigate('Main')}
                />
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
