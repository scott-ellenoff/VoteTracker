'use strict';

import React, {Component} from 'react';
import {Platform,
  Text,
  View,
  StyleSheet,
  Button,
  TextInput,
  AsyncStorage,
  Alert} from 'react-native';

export default class Signup extends Component {
  constructor(props) {
    super(props);
    this.state = {
      username: 'Username',
      email: 'Email',
      password1: 'Password',
      password2: 'Retype password',
      name: 'Name',
      district: 'District'
    };
  }

  static navigationOptions = {
    title: 'Signup',
  };

  render() {
    const {navigate} = this.props.navigation;
    return(
      <View style={styles.container}>
        <Text> Register For VoteTracker</Text>

        <TextInput
          style={styles.box}
          onChangeText={(text) => this.setState({username: text})}
          placeholder={this.state.username}
          autoCapitalize='none'
        />

        <TextInput
          style={styles.box}
          onChangeText={(text) => this.setState({email: text})}
          placeholder={this.state.email}
          autoCapitalize='none'
        />

        <TextInput
          style={styles.box}
          onChangeText={(text) => this.setState({password1: text})}
          placeholder={this.state.password1}
          autoCapitalize='none'
        />

        <TextInput
          style={styles.box}
          onChangeText={(text) => this.setState({password2: text})}
          placeholder={this.state.password2}
          autoCapitalize='none'
        />

        <TextInput
          style={styles.box}
          onChangeText={(text) => this.setState({name: text})}
          placeholder={this.state.name}
          autoCapitalize='none'
        />

        <TextInput
          style={styles.box}
          onChangeText={(text) => this.setState({district: text})}
          placeholder={this.state.district}
          autoCapitalize='none'

        />

        <Button
          title="Sign me up"
          onPress={this.signup}
        />
      </View>
    );
  }

  signup = () => {

    fetch('http://52.15.86.243:8080/api/v1/registration/', {
      method: 'POST',
      // POSTing to server
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username: this.state.username,
        email: this.state.email,
        password1: this.state.password1,
        password2: this.state.password2,
        name: this.state.name,
        district: this.state.district
      })
    })
    // end of fetch
      .then((response) => response.json())
      .then((json) => {
        console.log(json);
        const {navigate} = this.props.navigation;
        if (json.key) {
          Alert.alert('Registration Success', 
            'Congratulations! Your registration was accepted by the server.',
            [
              {text: 'Login Now', onPress: () => navigate('Home')},
              {text: 'Close Window', style: 'cancel'}

            ])
        } else {
          console.log(json);
          var counter = 0;
          var string_accumulator = ""; 
            if (json.password1) {
              counter = counter + 1;
              string_accumulator = string_accumulator + ' ' + 'Password too simple.' + '\n';
            }
            if (json.username) {
              counter = counter + 1;
              string_accumulator = string_accumulator + ' ' + 'Username already exists.' + '\n';
            }
            if (json.email) {
              counter = counter + 1;
              string_accumulator = string_accumulator + ' ' + 'Email is invalid.' + '\n';
            }
            if (json.district) {
              counter = counter + 1;
              string_accumulator = string_accumulator + ' ' + 'District must be integer.' + '\n';
            }
            if (counter == 0) {
              Alert.alert('Registration Failed',
              'Your input choices are allowed, but your two passwords do not match.',
              [
                {text: 'Go Back to Fix Errors', onPress: () => navigate('Signup'), style:'cancel'}
              ])
            } else {
            Alert.alert('Registration Failed',
              'Please correct ' + counter.toString() + ' problems:\n\n' + string_accumulator,
              [
                {text: 'Go Back to Fix Errors', onPress: () => navigate('Signup'), style:'cancel'}
              ])
          }
          }
        })
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
    borderWidth: 1,
    marginTop: 5,
    borderRadius: 5,
    textAlign: 'center'
  }
});
