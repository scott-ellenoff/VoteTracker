'use strict';

import React, {Component} from 'react';
import axios from 'axios';
import {FlatList, StyleSheet, View, Image, Text, TouchableHighlight} from 'react-native';
import ListItem from './Row';
import listData from './data';
import SelectLegislators from './selectLegislators';
import { AsyncStorage } from "react-native"




// Alter defaults after instance has been created

export default class Profile extends Component {
  static navigationOptions = {};


  constructor(props) {
    super(props);
    this.renderSeparator = this.renderSeparator.bind(this);
    this.success = this.success.bind(this);
    this.setScrollEnabled = this.setScrollEnabled.bind(this);

    this.state = {
      enable: true,
      data: listData,
      addMode: false,
      legialstors: null,
      followedLegislators: null
    };
  }
  componentDidMount(){
    const AUTH_TOKEN = this._retrieveData('token');
    console.log(AUTH_TOKEN)
    const instance = axios.create({
      baseURL: 'http://52.15.86.243:8080/api/v1/'
    });
    const key =  axios.get('user');
    console.log(key);
    instance.defaults.headers.common['Authorization'] = key;
    this.getUserInfo()
  }

  getUserInfo = () => {
    console.log('here')
  }
  _retrieveData = async (item) => {
    try {
      const value = await AsyncStorage.getItem(item);
      if (value !== null) {
        return value;
      }
    } catch (error) {
      // Error retrieving data
      console.log(error)
    }
  };
  // to follow legislator send PUT request to  users/v1 with followed: /api/v1/:LID in body to users/:id/ and have username in body as username
  // followed:  link to legialstor /api/v1/legislators/:LID, with a followed key for , "username": "admin",
  renderSeparator() {
    return (
      <View style={styles.separatorViewStyle}>
        <View style={styles.separatorStyle}/>
      </View>
    );
  }

  success(key) {
    const data = this.state.data.filter(item => item.key !== key);
    this.setState({
      data,
    });
  }

  setScrollEnabled(enable) {
    this.setState({
      enable,
    });
  }

  renderItem(item) {
    return (
      <ListItem
        text={item.key}
        success={this.success}
        setScrollEnabled={enable => this.setScrollEnabled(enable)}
      />
    );
  }

  updateLegislators = (val) => {
    console.log(val, 'here');
    this.setState((prevState) => {
      return {
        data: [...prevState.data, {key: val}],
        addMode: false
      }
    })
  };

  render() {
    const {navigate} = this.props.navigation;
    let {addMode} = this.state;
    if (!addMode) {
      return (
        <View>
          <Image source={require('../../assets/topbanner_page4.png')}/>
          <View>
            <FlatList
              style={this.props.style}
              data={this.state.data}
              ItemSeparatorComponent={this.renderSeparator}
              renderItem={({item}) => this.renderItem(item)}
              scrollEnabled={this.state.enable}
            />
          </View>
          <View style={styles.titleText}>
            <Text style={styles.titleText}> Select politicians to Follow</Text>
            <TouchableHighlight onPress={this.setState({addMode: true})}>
              <Image source={require('../../assets/page4_empty_politician.png')}/>

            </TouchableHighlight>
          </View>
        </View>
      )
    } else {
      return (
        <View>
          <Image source={require('../../assets/topbanner_page4.png')}/>
          <View>
            <FlatList
              style={this.props.style}
              data={this.state.data}
              ItemSeparatorComponent={this.renderSeparator}
              renderItem={({item}) => this.renderItem(item)}
              scrollEnabled={this.state.enable}
            />
          </View>
          <View>
            <SelectLegislators updateLegislators={this.updateLegislators}/>
          </View>
        </View>

      )
    }
    ;
  }
}

const styles = StyleSheet.create({
  separatorViewStyle: {
    flex: 1,
    backgroundColor: '#FFF',
  },
  separatorStyle: {
    height: 1,
    backgroundColor: '#000',
  },
  titleText: {
    fontSize: 20,
    justifyContent: 'center',
    alignItems: 'center',
    textAlign: 'center',
    textDecorationLine: 'underline'
  }
});
