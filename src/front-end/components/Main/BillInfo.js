'use strict';

import React, {Component} from 'react';
import {Text,
        View,
        StyleSheet,
        Button} from 'react-native';

export default class BillInfo extends Component {
    constructor(props) {
        super(props)

    }

    static navigationOptions = {
        title: 'Bill Info',
    };

    render() {
        const {navigate} = this.props.navigation;
        var bill = this.props.navigation.state.params.bill
        // NEED CONDITIONAL ON THE VOTED ON STUFF
        return(
            <View style={styles.container}>
                <Text> Bill Id: {bill.BID} {"\n"} </Text>

                <Text> Date Introduced: {bill.date_introduced} </Text>
                <Text> Voted On: {String(bill.voted_on)} </Text>
                <Text> Date Voted On: {bill.date_voted} {"\n"}</Text>

                <Text> Short Summary: {bill.description} {"\n"}</Text>

                <Text> Status: {bill.status} </Text>
                <Text> Chamber: {bill.chamber} {"\n"}</Text>

                <Text> Url: {bill.url} </Text>
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
