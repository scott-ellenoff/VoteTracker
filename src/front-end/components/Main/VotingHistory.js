'use strict';

/*
    IMPORTS
*/
import React, {Component} from 'react';
import {Text,
        View,
        StyleSheet,
        Button,
        ScrollView} from 'react-native';

/*
    Voting History Component
*/
export default class VotingHistory extends Component {
    /*
        Constructor to receive Main's props
    */
    constructor(props) {
        super(props)

    }

    render() {
        return(
            <ScrollView>
                {(this.props.bills).map((bill, key) => {
                    return (
                        <View key={key} style={styles.historyitems}>
                            <Text> {bill.name} </Text>

                            {bill.voted_on? (
                                <Text> Concluded </Text>
                            ) : (
                                <Text> Pending... </Text>
                            )}

                            <Button title="About"
                                    onPress={() => this.props.mainNav('BillInfo', {bill: bill})}
                            />
                        </View>
                    )
                })}
            </ScrollView>
        );
    }
}

/*
    Styling for JSX
*/
const styles = StyleSheet.create({
    historyitems: {
        flexDirection: "row"
    }
});
