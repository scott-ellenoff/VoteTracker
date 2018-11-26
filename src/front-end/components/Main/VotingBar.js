'use strict';

import React, {Component} from 'react';
import {Text,
        View,
        StyleSheet,
        Button,
        TouchableOpacity,
        Image} from 'react-native';

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

                {this.props.bills[billIndex]? (
                    <View style={styles.align}>
                        <Text> {this.props.bills[billIndex].BID} </Text>
                        <View style={styles.votebuttons}>

                            <TouchableOpacity
                            title="Nay"
                            style={styles.button}
                            onPress={() => this.setState({billIndex: nextIndex})}
                            >
                                <Image source={require('../../assets/nay.png')}
                                       style={styles.image}
                                />
                            </TouchableOpacity>

                            <TouchableOpacity
                            title="No Opinion"
                            style={styles.button}
                            onPress={() => this.setState({billIndex: nextIndex})}
                            >
                                <Image source={require('../../assets/idc.png')}
                                       style={styles.image}
                                />
                            </TouchableOpacity>

                            <TouchableOpacity
                            title="Yay"
                            style={styles.button}
                            onPress={() => this.setState({billIndex: nextIndex})}
                            >
                                <Image source={require('../../assets/yay.png')}
                                       style={styles.image}
                                />
                            </TouchableOpacity>

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
