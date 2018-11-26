'use strict';

import React, {Component} from 'react';
import {Text,
        View,
        StyleSheet,
        Button} from 'react-native';

export default class VotingBar extends Component {
    constructor(props) {
        super(props)
    }

    render() {
        return(
            <View style={styles.align}>
                <Text> {this.props.title} </Text>
                <View style={styles.votebuttons}>
                    <Button
                        title="Nay"
                    />
                    <Button
                        title="No Opinion"
                    />
                    <Button
                        title="Yay"
                    />
                </View>
                <Text> Progress: {this.props.progress}/{this.props.total} </Text>
            </View>
        );
    }

}

const styles = StyleSheet.create({
    votebuttons: {
        flexDirection: 'row'
    },
    align: {
        alignItems: 'center',
        backgroundColor: 'lightgray',
    }
});
