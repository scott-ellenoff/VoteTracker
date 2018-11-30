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
            loading: "initial"
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
        var main = this;

        console.log(user)

        // Once we receive the auth token
        AsyncStorage.getItem("key").then((value) => {
            this.setState({"token": value});
        })
        .then(res => {
            // Load in the votes the user has already made
            var config = {
                headers: {
                    'Authorization': "Token " + String(this.state.token)
                }
            }
            axios.get('http://52.15.86.243:8080/api/v1/votes/user_vote/', config)
            .then(res => {
                this.setState({userBills: res.data})
            })
            .catch(error => {
                console.log(error.response)
            });

            // Load in the votes the user has not already made
            main.setState({
                bills: user.unvoted,
                loading: false,
                progress: 0,
                total: user.unvoted.length,
            })
        });
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
                        bills={this.state.bills}
                        token={this.state.token}
                        progress={this.state.progress}
                        total={this.state.total}
                        mainNav={navigate}
                    />
                </View>

                <View style={styles.historybar}>
                    <VotingHistory
                        bills={this.state.userBills}
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
