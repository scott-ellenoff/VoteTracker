'use strict';

import React, {Component} from 'react';
import {Text,
        View,
        StyleSheet,
        Button} from 'react-native';

export default class VotingBar extends Component {
    render() {
        return(
            <View style={styles.align}>
                <Text> Abortion, 20-Week Ban </Text>
                <View style={styles.votebuttons}>
                    <Button
                        title="INFO"
                    />
                    <Button
                        title="Nay"
                    />
                    <Button
                        title="IDC"
                    />
                    <Button
                        title="Yay"
                    />
                    <Button
                        title="NEXT"
                    />

                </View>
            </View>
        );
    }

}

const styles = StyleSheet.create({
    votebuttons: {
        flexDirection: "row"
    },
    align: {
        alignItems: 'center'
    }
});
