'use strict';

import React, {Component} from 'react';
import {Text,
        View,
        StyleSheet,
        Button,
        Linking} from 'react-native';

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
        return(
            <View style={styles.container}>
                <Text>{"\n"}Bill {bill.BID}{"\n"}</Text>

                <View
                  style={{
                    borderBottomColor: 'black',
                    borderBottomWidth: 5,
                  }}
                 />

                <Text>{"\n"}Information{"\n"}</Text>
                <Text>Deliberated on by the {bill.chamber}</Text>
                <Text>Introduced on {bill.date_introduced}</Text>
                {bill.voted_on ? (
                    <Text>Voted on {bill.date_voted}{"\n"}</Text>
                ) : (
                    <Text>This bill has not been voted on{"\n"}</Text>
                )}

                <View
                  style={{
                    borderBottomColor: 'black',
                    borderBottomWidth: 5,
                  }}
                 />

                <Text>{"\n"}Short Summary{"\n\n"}{bill.description} {"\n"}</Text>

                <View
                  style={{
                    borderBottomColor: 'black',
                    borderBottomWidth: 5,
                  }}
                 />

                <Text>{"\n"}Status{"\n\n"}{bill.status}{"\n"}</Text>

                <View
                  style={{
                    borderBottomColor: 'black',
                    borderBottomWidth: 5,
                  }}
                  />

                <Text>{"\n"}</Text>

                <Button title="Learn Even More"
                        onPress={ ()=>{ Linking.openURL(bill.url)}} />
            </View>
        );
    }

}

const styles = StyleSheet.create({
    container: {
        padding: 10
    },

    votebuttons: {
        flexDirection: "row"
    },
});
