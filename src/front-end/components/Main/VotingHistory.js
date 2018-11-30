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

        this.state = {
            bills: ""
        }
    }

    getBills() {
        console.log(this.props.token)

        var config = {
            headers: {
                'Authorization': "Token " + String(this.props.token)
            }
        }

        axios.get('http://52.15.86.243:8080/api/v1/votes/user_vote/', config)
        .then(res => {
            console.log(res);
            console.log(res.data);
            this.setState({bills: res.data})
        })
        .catch(error => {
            console.log(error.response)
        });
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
