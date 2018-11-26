'use strict';

import axios from 'axios'

import React, {Component} from 'react';
import {Text,
        View,
        StyleSheet,
        Button,
        ScrollView} from 'react-native';

import VotingBar from "./VotingBar.js";
import Boot from "./Boot.js"

export default class Main extends Component {
    constructor(props) {
        super(props)

        this.state = {
            loading: "initial"
        }
    }

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

            </View>
        );
    }
}

const styles = StyleSheet.create({
    container: {
        alignItems: 'center',
        paddingTop: 5,
        paddingRight: 50,
        paddingLeft: 50,
    },
    votingbar: {
        alignItems: "center",
        width: 400,
        height: 200,
        backgroundColor: "white"
    }
});
