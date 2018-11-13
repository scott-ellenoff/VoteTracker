'use strict'

import React, {Component} from 'react';
import {Platform,
        Text,
        View,
        StyleSheet,
        Button} from 'react-native';

export default class Main extends Component {
    static navigationOptions = {
        title: 'Main',
    }

    render() {
        const {navigate} = this.props.navigation
        return(
            <View style={styles.container}>
                <Text> Main Page </Text>
                <Button
                    title="Go to Profile Screen"
                    onPress={() => navigate('Profile')}
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
