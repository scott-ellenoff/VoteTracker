import React, { Component } from 'react';
import { Alert, AppRegistry, Platform,
  StyleSheet, Text, TouchableHighlight,
  TouchableOpacity, TouchableNativeFeedback,
  TouchableWithoutFeedback, View ,TextInput} from 'react-native';

export default class SelectLegislators extends Component {
  constructor(props) {
    super(props);
    this.state = {
      firstname: 'First Name',
      lastname: 'Last Name'
    };
  }

  _onPressButton() {
    Alert.alert('You tapped the button!')
  }

  _onLongPressButton() {
    Alert.alert('You long-pressed the button!')
  }


  render() {
    return (
      <View style={styles.container}>
        <View>
        <TextInput
          style={styles.textBox}
          onChangeText={(text) => this.setState({firstname: text})}
          value={this.state.firstname}
        />
        <TextInput
          style={styles.textBox}
          onChangeText={(text) => this.setState({lastname: text})}
          value={this.state.lastname}
        />
        </View>

      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    paddingTop: 60,
    alignItems: 'center'
  },
  button: {
    marginBottom: 30,
    width: 260,
    alignItems: 'center',
    backgroundColor: '#2196F3'
  },
  buttonText: {
    padding: 20,
    color: 'white'
  },
  textBox: {
    height: 40,
    width: 150,
    backgroundColor: 'white',
    borderColor: 'black',
    borderWidth: 1
  }
});
