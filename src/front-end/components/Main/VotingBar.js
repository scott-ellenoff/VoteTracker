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
        TouchableOpacity,
        Image} from 'react-native';

/*
    Voting Bar Component
*/
export default class VotingBar extends Component {
    /*
        Constructor to receive Main's props and initialize incrementing through bills
    */
    constructor(props) {
        super(props)
        this.state = {
            billIndex: 0
        }
        this.postVote = this.postVote.bind(this)
    }

    postVote(option, currIndex) {
        // Once I vote
        // axios.post(header: {Authorization: "Token value"} body:{bill: "/api/v1/bills/bid", "vote": "YNA"})
        console.log(this.props.token)

        var config = {
            headers: {
                'Authorization': "Token " + String(this.props.token)
            }
        }

        var voteResponse = "Y"
        if (option == "nay") {
            voteResponse = "N"
        } else if (option == "idc") {
            voteResponse = "A"
        }
        var details = {
            bill: "/api/v1/bills/" + String(this.props.bills[currIndex].BID) + '/',
            vote: voteResponse,
        }

        axios.post('http://52.15.86.243:8080/api/v1/votes/user_vote/', details, config)
        .then(res => {
            console.log(res);
            console.log(res.data);
        })
        .catch(error => {
            console.log(error.response)
        });

        var nextIndex = currIndex + 1
        this.setState({billIndex: nextIndex})
    }

    render() {
        // To Increment Through Bills
        var billIndex = this.state.billIndex;

        // To Create Yay, Nay, IDC Buttons
        var voteOptions = ['yay', 'idc', 'nay'];
        return(
            <View>

                {this.props.bills[billIndex]? (
                    <View style={styles.align}>

                        <Text> {this.props.bills[billIndex].BID} </Text>
                        <View style={styles.votebuttons}>

                            {voteOptions.map((option, key) => {
                                var req = require('../../assets/yay.png');
                                if (option == 'nay') {
                                    req = require('../../assets/nay.png')
                                } else if (option == 'idc') {
                                    req = require('../../assets/idc.png')
                                }
                                return (
                                    <TouchableOpacity
                                    title={option}
                                    key={key}
                                    style={styles.button}
                                    onPress={() => this.postVote(option, billIndex)}
                                    >

                                    <Image source={req}
                                           style={styles.image}
                                    />
                                    </TouchableOpacity>
                                )
                            })}

                        </View>
                        <Text> Progress: {this.state.billIndex}/{this.props.total} </Text>
                        <Button
                            title="Learn More"
                            onPress={() => this.props.mainNav('BillInfo', {bill: this.props.bills[billIndex]})}
                        />
                    </View>
                ) : (
                    <View style={styles.align}>
                        <Text> You’re Totally Caught Up! </Text>
                        <Text> We update regularly, so check back soon </Text>
                        <Text> for more bills and voting information </Text>
                    </View>
                )}

            </View>
        );
    }
}

/*
    Styling for JSX
*/
const styles = StyleSheet.create({
    votebuttons: {
        flexDirection: 'row'
    },
    align: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: 'white',
    },
    button: {
        padding: 25
    },
    image: {
        width: 40,
        height: 40,
        resizeMode: 'contain'
    }
});
