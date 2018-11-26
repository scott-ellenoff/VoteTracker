'use strict';

import axios from 'axios'

import React, {Component} from 'react';
import {Text,
        View,
        StyleSheet,
        Button,
        ScrollView} from 'react-native';

import VotingBar from "./VotingBar.js";

export default class Main extends Component {
    constructor(props) {
        super(props)

        this.state = {
            title: "[TITLE]",
            loading: "initial"
        }
    }

    static navigationOptions = {
        title: 'Main',
    };

    componentWillMount() {
        this.setState({loading: "true"})

        var main = this
        axios.get('http://52.15.86.243:8080/bills/')
            .then(function (response) {
                let data = response.data.slice(0, 10)
                main.setState({bills: data,
                               loading: false,
                               progress: 0,
                               total: data.length
                           })
            })
            .catch(function (error) {
                console.log(error)
            })
    }

    render() {
        const {navigate} = this.props.navigation;

        // Initialize
        if (this.state.loading == 'initial') {
            return <Text>Intializing...</Text>;
        }

        // Load
        if (this.state.loading) {
            return <Text>Loading...</Text>;
        }

        // Render
        return(
            <View style={styles.container}>

                <View>
                    <VotingBar
                        title={this.state.bills[2].BID}
                        progress={this.state.progress}
                        total={this.state.total}
                    />
                    <Button
                        color="green"
                        title="Learn More"
                        onPress={() => navigate('BillInfo', {bill: this.state.bills[2]})}
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

// onPress={() => navigate('Profile')}
