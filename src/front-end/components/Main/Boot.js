'use strict';

/*
    IMPORTS
*/
import React, {Component} from 'react';
import {Text,
        View,
        StyleSheet,
        StatusBar,
        ActivityIndicator} from 'react-native';

/*
    Boot Screen Component
*/
export default class Boot extends Component {
    /*
        Constructor for passing of text props
    */
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

/*
    Styling for JSX
*/
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
