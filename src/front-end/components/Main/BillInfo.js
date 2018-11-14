'use strict';

import React, {Component} from 'react';
import {Text,
        View,
        StyleSheet,
        Button} from 'react-native';

export default class BillInfo extends Component {
    static navigationOptions = {
        title: 'BillInfo',
    };

    render() {
        const {navigate} = this.props.navigation;
        return(
            <View style={styles.container}>
                <Text> Bill Info Here </Text>
            </View>
        );
    }

}

const styles = StyleSheet.create({
    container: {
        alignItems: 'center',
        paddingTop: 100,
        paddingRight: 50,
        paddingLeft: 50
    },

    votebuttons: {
        flexDirection: "row"
    },
});
