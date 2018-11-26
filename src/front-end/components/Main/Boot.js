'use strict';

import axios from 'axios'

import React, {Component} from 'react';
import {Text,
        View,
        StyleSheet,
        StatusBar,
        ActivityIndicator} from 'react-native';

export default class Boot extends Component {
    constructor(props) {
        super(props)
    }

    render() {
        return(
            <View style={styles.container}>
                <StatusBar barStyle="light-content"/>
                <Text style={styles.text}> {this.props.text} </Text>
                <ActivityIndicator color={'black'}/>
            </View>
        );
    }
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        paddingTop: 250,
        alignItems: 'center'
    },
    text: {
        color : 'black',
        fontSize : 18
    }
});
