'use strict';

/*
    IMPORTS
*/
import axios from 'axios'

import React, {Component} from 'react';
import {Text,
        Image,
        View,
        StyleSheet,
        Button,
        Linking,
        TouchableOpacity} from 'react-native';

/*
    Bill Information Component
*/
export default class BillInfo extends Component {
    /*
        Constructor for passing of bill props
    */
    constructor(props) {
        super(props)
    }

    /*
        NavOptions for changing of Header title
    */
    static navigationOptions = {
        title: 'Bill Info',
    };

    render() {
        // Pulling props from navigation
        var bill = this.props.navigation.state.params.bill

        return(
            <View>
            <View style={styles.container}>
                <Text style={styles.heading}>{"\n"}Bill{"\n"}</Text>
                <Text style={styles.body}>{bill.name}</Text>

                <Text style={styles.heading}>{"\n"}Information{"\n"}</Text>
                <Text style={styles.body}>Deliberated on by the {bill.chamber}</Text>
                <Text style={styles.body}>Introduced on {bill.date_introduced}</Text>
                {bill.voted_on ? (
                    <Text style={styles.body}>Voted on {bill.date_voted}</Text>
                ) : (
                    <Text style={styles.body}>This bill has not been voted on</Text>
                )}

                <Text style={styles.heading}>{"\n"}Short Summary{"\n"}</Text>
                <Text style={styles.body}>{bill.description}</Text>

                <Text style={styles.heading}>{"\n"}Status{"\n"}</Text>
                <Text style={styles.body}>{bill.status}{"\n"}</Text>

                <Text>{"\n"}</Text>

                <TouchableOpacity title="URL"
                        style={styles.urlstyle}
                        onPress={ ()=> { Linking.openURL(bill.url) } }>

                        <Text style={styles.urltext}> Learn More at GovTrack.us  </Text>
                </TouchableOpacity>

            </View>
            </View>
        );
    }

}

/*
    Styling for JSX
*/
const styles = StyleSheet.create({
    urlstyle: {
        borderRadius: 10,
        borderWidth: 1,
        borderColor: '#F33E35',
        marginLeft: 5,
        marginRight: 5,
    },
    urltext : {
        color: '#F33E35',
        fontSize: 16,
        textAlign: 'center',
    },
    heading: {
        fontSize: 16,
        color: '#F33E35',

    },
    body: {
        color: "#0C314A"
    },
    container: {
        padding: 10,
        backgroundColor: 'white',
        height: 1000
    },

    votebuttons: {
        flexDirection: "row"
    },
});
