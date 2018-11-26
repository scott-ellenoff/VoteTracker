'use strict';

import React, {Component} from 'react';
import {Text,
        View,
        StyleSheet,
        Button} from 'react-native';

export default class VotingBar extends Component {
    constructor(props) {
        super(props)

        this.state = {
            billIndex: 0
        }
    }

    render() {
        var billIndex = this.state.billIndex
        var nextIndex = this.state.billIndex + 1
        return(
            <View>

                {this.props.bills[billIndex] &&
                    <View style={styles.align}>
                        <Text> {this.props.bills[billIndex].BID} </Text>
                        <View style={styles.votebuttons}>
                            <Button
                                title="Nay"
                                onPress={() => this.setState({billIndex: nextIndex})}
                            />
                            <Button
                                title="No Opinion"
                                onPress={() => this.setState({billIndex: nextIndex})}
                            />
                            <Button
                                title="Yay"
                                onPress={() => this.setState({billIndex: nextIndex})}
                            />
                        </View>
                        <Text> Progress: {this.state.billIndex}/{this.props.total} </Text>
                        <Button
                            title="Learn More"
                            onPress={() => this.props.mainNav('BillInfo', {bill: this.props.bills[billIndex]})}
                        />
                    </View>
                }

            </View>
        );
    }

}

const styles = StyleSheet.create({
    votebuttons: {
        flexDirection: 'row'
    },
    align: {
        alignItems: 'center',
        backgroundColor: 'lightgray',
    }
});
