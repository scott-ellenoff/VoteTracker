'use strict';

import React, {Component} from 'react';
import {Platform,
        Text,
        View,
        StyleSheet,
        Button,
        TextInput} from 'react-native';

export default class Home extends Component {
    constructor(props) {
        super(props);
        this.state = {
                        username: 'Username',
                        password: 'Password'
                    };
     }

    static navigationOptions = {
        title: 'Home',
    };

    render() {
        const {navigate} = this.props.navigation;
        return(
            <View style={styles.container}>
                <Text> VoteTracker </Text>

                <TextInput
                    style={styles.box}
                    onChangeText={(text) => this.setState({username: text})}
                    value={this.state.username}
                />
                <TextInput
                    style={styles.box}
                    onChangeText={(text) => this.setState({password: text})}
                    value={this.state.password}
                />

                <Button
                    title="Login"
                    onPress={() => navigate('Main')}
                />
            </View>
        );
    }

}

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    paddingTop: 200,
    paddingRight: 50,
    paddingLeft: 50,
  },
  box: {
      height: 40,
      width: 150,
      backgroundColor: 'white',
      borderColor: 'black',
      borderWidth: 1
  }
});
