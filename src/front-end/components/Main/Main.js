'use strict';

import React, {Component} from 'react';
import {Text,
        View,
        StyleSheet,
        Button,
        ScrollView} from 'react-native';

import VotingBar from "./VotingBar.js";

export default class Main extends Component {
    static navigationOptions = {
        title: 'Main',
    };

    render() {
        const {navigate} = this.props.navigation;
        return(
            <View style={styles.container}>

                <View>
                    <VotingBar
                        title="[TITLE]"
                        progress="[X]"
                        total="[Y]"
                    />
                    <Button
                        color="green"
                        title="Learn More"
                        onPress={() => navigate('BillInfo')}
                    />
                </View>

                


                <View style={{paddingTop: 200}}>
                    <Button
                        title="Go to Profile Screen"
                        onPress={() => navigate('Profile')}
                    />
                </View>
            </View>
        );
    }

}

const styles = StyleSheet.create({
    container: {
        alignItems: 'center',
        paddingTop: 100,
        paddingRight: 50,
        paddingLeft: 50,
    },
    scrollview: {
        height: 400,
        flex: 1
    }

});
