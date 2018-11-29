'use strict';

import React, {Component} from 'react';
import {
  Platform,
  Text,
  View,
  StyleSheet,
  Button,
  TextInput,
  AsyncStorage,
  Alert
} from 'react-native';

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
    return (
      <View style={styles.container}>
        <Text> VoteTracker </Text>

        <TextInput
          style={styles.box}
          onChangeText={(text) => this.setState({username: text})}
          placeholder={this.state.username}
          autoCapitalize='none' //added
        />

        <TextInput
          style={styles.box}
          onChangeText={(text) => this.setState({password: text})}
          placeholder={this.state.password}
          autoCapitalize='none' //added
          secureTextEntry={true}
        />

        <Button
          title="Login"
          onPress={() => {
            const success = this.login();
            if (success) {
              navigate('Main');
            }
          }}
        />

        <Button
          title="Sign Up"
          onPress={() => navigate('Signup')}
        />

      </View>
    );
  }

  login = () => {
    fetch('http://52.15.86.243:8080/rest-auth/login/', {
      method: 'POST',
      // POSTing to server
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username: this.state.username,
        password: this.state.password,
      })
    })
      .then((response) => response.json())
      .then((json) => {
        if (json.key) {
          // if there is a token in the object returned by the server
          AsyncStorage.setItem('key', json.key); //syntax is setItem(key,value)
          // save the token value in AsyncStorage, a global storage

          // AsyncStorage.getItem('key')
          //   .then((value) => Alert.alert('Login succeeded, key is saved, its value is', value)) // this is the key
          this.props.navigation.navigate('Main');
          return true;
        } else {
          Alert.alert("Login Error", 'Login failed');
          return false;
        }
      }).catch((err) => console.log(err))
      .done()
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
