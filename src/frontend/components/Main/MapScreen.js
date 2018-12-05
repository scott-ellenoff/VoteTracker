'use strict';

/*
    IMPORTS
*/
import React, {Component} from 'react';
import {ScrollView,
        View,
        StyleSheet,
        Image} from 'react-native';

/*
    Voting Bar Component
*/
export default class MapScreen extends Component {
    constructor(props) {
        super(props)

    }

    render() {
        var bill = this.props.navigation.state.params.bill
        var url = 'https://s3.us-east-2.amazonaws.com/votetrackermaps/' + String(bill.BID) + '.png'
        return(
            <ScrollView maximumZoomScale={3}>
                <Image source={{uri: url}} style={styles.map}/>
            </ScrollView>
        );
    }
}

/*
    Styling for JSX
*/
const styles = StyleSheet.create({
    map: {
        transform: [{ rotate: '90deg'}],
        width: 800,
        height: 400,
        top: 100,
        right: 200
    }
});
