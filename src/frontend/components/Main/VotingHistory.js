'use strict';

/*
    IMPORTS
*/
import React, {Component} from 'react';
import {Text,
        View,
        StyleSheet,
        Button,
        ScrollView,
        TouchableOpacity} from 'react-native';

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

                            <Text style={styles.name}> {bill.BID} </Text>

                            {bill.voted_on? (
                                <Text style={styles.status}> Resolved  </Text>
                            ) : (
                                <Text style={styles.status}> Pending.. </Text>
                            )}

                            <TouchableOpacity title="About"
                                    style={styles.about}
                                    onPress={() => this.props.mainNav('BillInfo', {bill: bill})}>

                                    <Text style={{color: '#F33E35'}}> About </Text>

                            </TouchableOpacity>

                            <TouchableOpacity title="Map"
                                    style={styles.map}
                                    onPress={() => this.props.mainNav('MapScreen', {bill: bill})}>

                                    <Text style={{color: '#F33E35'}}> Map </Text>

                            </TouchableOpacity>
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
        flexDirection: "row",
        alignItems: 'center',
        paddingBottom: 10,
        marginTop: 10,
        borderBottomColor: 'lightgray',
        borderBottomWidth: 0.5,
    },
    name: {
        textAlign: 'left',
        width: 160,
        color: '#0C314A'
    },
    status: {
        color: '#0C314A'
    },
    about: {
        borderRadius: 10,
        borderWidth: 1,
        borderColor: '#F33E35',
        marginLeft: 5,
        marginRight: 5,
    },
    map: {
        borderRadius: 10,
        borderWidth: 1,
        borderColor: '#F33E35',
        marginLeft: 5,
        marginRight: 5,
    },
});
