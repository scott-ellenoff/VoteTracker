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
        Linking} from 'react-native';

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

        var main = this;
        axios.get('http://52.15.86.243:8080/api/v1/bills/')
            .then(function (response) {
                const data = response.data.slice(0, 10);
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
                        progress={this.state.progress}
                        total={this.state.total}
                        mainNav={navigate}
                    />
                </View>

                <View style={styles.historybar}>
                    <VotingHistory
                        bills={this.state.bills}
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
