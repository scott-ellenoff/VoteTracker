'use strict';

import React, {Component} from 'react';
import {
  Text,
  View,
  StyleSheet,
  Image
} from 'react-native';


class LogoTitle extends React.Component {
  render() {
    return (
      <Image
        source={require('../../assets/topbanner_page4.png')}

      />
    );
  }
}

export default class Profile extends Component {
  static navigationOptions = {};

  render() {
    const selected_pol = new Array(20);

    const selected_images = selected_pol.map(val => {
      return <Image source={require('../../assets/page4_empty_politician.png')}/>
    });
    return (
      <View>
        <LogoTitle style={styles.topImage}/>
        <Text style={styles.titleText}>Select politicians to Follow</Text>

      </View>
    );
  }

}

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    paddingTop: 200,
    paddingRight: 50,
    paddingLeft: 50
  },
  titleText: {
    fontSize: 20,
    // fontWeight: 'bold',
    textAlign: 'center',
    textDecorationLine: 'underline'
  },
  topImage: {
    justifyContent: 'center',
    alignItems: 'center',
  }

});
