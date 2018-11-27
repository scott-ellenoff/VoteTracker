'use strict';

/*
    IMPORTS
*/
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
    }

    render() {
        // To Increment Through Bills
        var billIndex = this.state.billIndex
        var nextIndex = this.state.billIndex + 1

        // To Create Yay, Nay, IDC Buttons
        var voteOptions = ['yay', 'idc', 'nay']
        return(
            <View>

                {this.props.bills[billIndex]? (
                    <View style={styles.align}>
                        <Text> {this.props.bills[billIndex].BID} </Text>
                        <View style={styles.votebuttons}>

                            {voteOptions.map((option, key) => {
                                var req = require('../../assets/yay.png')
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
                                    onPress={() => this.setState({billIndex: nextIndex})}
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
                    <View>
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
        alignItems: 'center',
        backgroundColor: 'white',
    },
    button: {
        padding: 25
    },
    image: {
        width: 50,
        height: 50,
        resizeMode: 'contain'
    }
});
