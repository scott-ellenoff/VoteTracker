'use strict';

import React, {Component} from 'react';
import {Text,
        View,
        StyleSheet,
        Button} from 'react-native';

import VotingBar from "./VotingBar.js";

export default class Main extends Component {
    static navigationOptions = {
        title: 'Main',
    };

    render() {
        const {navigate} = this.props.navigation;
        return(
            <View style={styles.container}>

                <VotingBar
                    title="20-Day Abortion Ban"
                    progress={1}
                    total={10}
                />


                <View style={{paddingTop: 200}}></View>
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
        paddingTop: 100,
        paddingRight: 50,
        paddingLeft: 50
    },

    votebuttons: {
        flexDirection: "row"
    },
});
