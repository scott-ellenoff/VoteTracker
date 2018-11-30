'use strict';

/*
    IMPORTS
*/
import axios from 'axios'

import React, {Component} from 'react';
import {Text,
        View,
        StyleSheet,
        Button,
        ScrollView,
        Linking,
        AsyncStorage} from 'react-native';

import VotingBar from "./VotingBar.js";
import VotingHistory from "./VotingHistory.js"
import Boot from "./Boot.js"

/*
    Main Screen Component
*/
export default class Main extends Component {
    /*
        Constructor to initialize state as "loading"
    */
    constructor(props) {
        super(props);

        this.state = {
            loading: "initial",
            unvotedBills: [],
            votedBills: [],
        }
    }

    /*
        Header Title as Main, and Header button moving user to Profile screen
    */
    static navigationOptions = ({ navigation }) => {
        return {
            title: 'Main',
            headerRight: (
                <Button
                    title="Profile"
                    onPress={() => navigation.navigate('Profile')}
                />
            )
        }
    };

    /*
        Loading User API Information to state (finish loading bills)
    */
    componentWillMount() {
        this.setState({loading: "true"});

        var user = this.props.navigation.state.params.user
        var key = this.props.navigation.state.params.key

        var config = {
            headers: {
                'Authorization': "Token " + String(key)
            }
        }
        // Load in the votes the user has already made
        var votedBills = []
        for (var i = 0; i < user.voted.length; i++) {
            axios.get(user.voted[i], config)
            .then(billInfo => {
                var all = this.state.votedBills
                all.push(billInfo.data)
                this.setState({votedBills: all})
            })
            .catch(error => {
                console.log(error.response)
            });
        }

        // Load in the votes the user has not already made
        var unvotedBills = []
        for (var i = 0; i < user.unvoted.length; i++) {
            axios.get(user.unvoted[i], config)
            .then(billInfo => {
                var all = this.state.unvotedBills
                all.push(billInfo.data)
                this.setState({unvotedBills: all})
            })
            .catch(error => {
                console.log(error.response)
            });
        }

        console.log(user.voted)

        this.setState({
            unvotedBills: unvotedBills,
            votedBills: votedBills,
            loading: false,
            progress: 0,
            total: user.unvoted.length,
        })

    }

    render() {
        const {navigate} = this.props.navigation;
        // Initialize
        if (this.state.loading === 'initial') {
            return <Boot text="Initializing..."/>
        }

        // Load
        if (this.state.loading) {
            return <Boot text="Loading..."/>
        }

        // Render
        return(
            <View style={styles.container}>

                <View style={styles.votingbar}>
                    <VotingBar
                        bills={this.state.unvotedBills}
                        token={this.props.navigation.state.params.key}
                        progress={this.state.progress}
                        total={this.state.total}
                        mainNav={navigate}
                    />
                </View>

                <View style={styles.historybar}>
                    <VotingHistory
                        bills={this.state.votedBills}
                        mainNav={navigate}
                    />
                </View>

            </View>
        );
    }
}

/*
    Styling for JSX
*/
const styles = StyleSheet.create({
    container: {
        alignItems: 'center',
        padding: 10,
    },
    votingbar: {
        alignItems: "center",
        width: 400,
        height: 175,
        backgroundColor: "white"
    },
    historybar: {
        marginTop: 10,
        alignItems: "center",
        width: 400,
        height: 400,
        backgroundColor: "white"
    }
})
