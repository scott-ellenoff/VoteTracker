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
      username: 'Choose username',
      email: 'Your email',
      password1: 'Choose smart password',
      password2: 'Retype password',
      name: 'Your name',
      district: 'District (Integer)'
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
        if (json.key) {
          Alert.alert('Registration was successful, key is (not saved), its value is', json.key)
        } else {
          Alert.alert('Registration was NOT successful')
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
    borderWidth: 1
  }
});
