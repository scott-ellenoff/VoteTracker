'use strict';

/*
    IMPORTS
*/
import React, {Component} from 'react';
import {Text,
        View,
        StyleSheet,
        Button,
        Linking} from 'react-native';

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
            <View style={styles.container}>
                <Text>{"\n"}Bill {bill.name}{"\n"}</Text>

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
                        onPress={ ()=> { Linking.openURL(bill.url) } }/>
            </View>
        );
    }

}

/*
    Styling for JSX
*/
const styles = StyleSheet.create({
    container: {
        padding: 10
    },

    votebuttons: {
        flexDirection: "row"
    },
});
