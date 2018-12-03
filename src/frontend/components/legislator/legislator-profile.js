'use strict';

/*
    IMPORTS
*/
import axios from 'axios'

import React, {Component} from 'react';
import {
  Text,
  View,
  StyleSheet,
  Button,
  ScrollView,
  Linking,
  AsyncStorage
} from 'react-native';
import Voting from './voting';

import Boot from "../Main/Boot.js"
import BillInfo from "../Main/BillInfo";

/*
    Main Screen Component
*/
export default class LegislatorProfile extends Component {
  /*
      Constructor to initialize state as "loading"
  */
  constructor(props) {
    super(props);

    this.state = {
      loading: true,
      legislator: null,
      bills: null
    }
  }

  /*
      Header Title as Main, and Header button moving user to Profile screen
  */
  static navigationOptions = ({navigation}) => {
    return {
      title: 'Main',
      // headerRight: (
      //   <Button
      //     title="Profile"
      //     onPress={() => navigation.navigate('Profile')}
      //   />
      // )
    }
  };

  /*
      Loading User API Information to state (finish loading bills)
  */
  componentWillMount() {
    const key = this.props.navigation.state.params.key;
    const config = {
      headers: {
        'Authorization': "Token " + String(key)
      }
    };

    // LID: "A000360"
    // affiliation: "Republican"
    // detail: "http://52.15.86.243:8080/api/v1/legislators/A000360/"
    // district: 0
    // dwnominate: 0
    // fullname: "Lamar Alexander"
    // senator: true
    // state: "TN"
    // url: "https://www.alexander.senate.gov/public"

    const link = this.props.navigation.state.params.legislator;

    axios.get(link, config)
      .then(data => {
          this.setState({legislator: data.data});
          return data.data.LID;
        }
      )
      .then((LID)  => {
        console.log(LID);

        axios.get(`http://52.15.86.243:8080/api/v1/votes/?legislator=${LID}`, config)
          .then(data => {
            console.log(data.data);
            const bills = data.data.results.reduce((acc, cur) => {
              acc.push(cur.bill);
              return acc;
              }
              , []);
              this.setState({votes: data.data, loading:false, bills: bills});
            }
          )
      })
      .catch(error => {
        console.log(error.response)
      });
  }

  render() {
    const {navigate} = this.props.navigation;
    // Load
    if (this.state.loading) {
      return <Boot text="Loading..."/>
    }

    // Render
    return (
      <View style={styles.container}>
        <Text>{this.state.legislator.fullname}</Text>
        <View>
          <Voting

            bills={this.state.votes}
            mainNav={navigate}
          />
        </View>

      </View>
    );
  }
}

// LID: "B001270"
// affiliation: "Democrat"
// detail: "http://52.15.86.243:8080/api/v1/legislators/B001270/"
// district: 37
// dwnominate: 0
// fullname: "Karen Bass"
// senator: false
// state: "CA"
// url: "https://bass.house.gov"

/*
    Styling for JSX
*/
const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    padding: 10,
  },
  votingbar: {
    alignItems: "center",
    width: 400,
    height: 175,
    backgroundColor: "white"
  },
  historybar: {
    marginTop: 10,
    alignItems: "center",
    width: 400,
    height: 400,
    backgroundColor: "white"
  }
})
