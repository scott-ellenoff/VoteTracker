'use strict';

import React, {Component} from 'react';
import axios from 'axios';
import {FlatList, StyleSheet, View, Image, Text, TouchableHighlight, ScrollView, ListView} from 'react-native';
import ListItem from './Row';
import listData from './data';
import SelectLegislators from './selectLegislators';
import {AsyncStorage} from 'react-native'
import Boot from "../Main/Boot";
import {groupBy} from "./utils";
import Swipeout from 'react-native-swipeout';

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
      legislators: null,
      followedLegislators: null,
      UID: "",
      userLink: "",
      userFirstName: "",
      userID: "",
      district: null,
      loading: true,
      axiosInstance: null,
      username: '',
      token: null,
      pickerSelected: '',
      byLid: null,
      userInfo: null,
      matches: null,
      matchData: [],
      matchesLoaded: 0
    };
  }

  componentDidMount() {
    const AUTH_TOKEN = AsyncStorage.getItem('key')
      .then((v) => {
        this.setState({token: v});
        return v
      });
    const user = AsyncStorage.getItem('user')
      .then((value) => JSON.parse(value)[0])
      .then((userInfo) => {
        console.log(userInfo);
        const instance = axios.create({
          baseURL: 'http://52.15.86.243:8080/api/v1/'
        });
        instance.defaults.headers.common['Authorization'] = AUTH_TOKEN;
        console.log(userInfo);
        this.setState({
          followedLegislators: userInfo.followed,
          UID: userInfo.UID,
          district: userInfo.district,
          userFirstName: userInfo.name,
          userID: userInfo.id,
          axiosInstance: instance,
          username: userInfo.username,
          userInfo: userInfo,
          matches: userInfo.matched
        }, this.startComponent)
      }); // this is the key

  }

  startComponent() {
    this.updateMatchData();
    this.getLegislators();
  }

  getLegislators() {
    const token = this.state.token;
    console.log(token);
    axios.get('http://52.15.86.243:8080/api/v1/legislators/', {
      headers: {
        'Content-Type': 'multipart/form-data',
        "Authorization": `Token ${token}`
      }
    })
      .then((data) => {
        console.log(data);
        return data
      })
      .then(d => {
        const byLid = groupBy(d.data, 'LID');

        this.setState({
          legislators: d.data,
          loading: false,
          byLid: byLid,
          pickerSelected: d.data[0].LID,
          leg: d.data[0]
        })
      })
      .catch((err) => console.log(err))

  }

  updateFollowLegislators = () => {
    const {username, userID, token, followedLegislators} = this.state;
    const form = new FormData();

    form.append('username', username);
    followedLegislators.forEach((leg) => form.append('followed', leg));
    console.log("all legislators", form, followedLegislators);
    axios.put(`http://52.15.86.243:8080/api/v1/users/${userID}/`, form, {
      headers: {
        'Content-Type': 'multipart/form-data',
        "Authorization": `Token ${token}`
      }
    }).then(d => {
      this.setState({followedLegislators: d.data.followed, matches: d.data.matched}, this.updateMatchData);
    })
      .catch((err) => console.log(err));
  };

  updateMatchData = () => {
    console.log('here');
    const {token} = this.state;
    axios.get('http://52.15.86.243:8080/api/v1/matches/', {
      headers: {
        'Content-Type': 'multipart/form-data',
        "Authorization": `Token ${token}`
      }
    }).then((data) => {
      this.setState({matchData: data.data})
    })
  };

  renderSeparator() {
    return (
      <View style={styles.separatorViewStyle}>
        <View style={styles.separatorStyle}/>
      </View>
    );
  }

  success(key) {
    console.log(key, 'in success');
    const data = this.state.followedLegislators.filter(item => this.state.byLid[item.split('/')[6]][0].fullname !== key);
    this.setState({
      followedLegislators: data,
    }, this.updateFollowLegislators);
  }

  setScrollEnabled(enable) {
    this.setState({
      enable,
    });
  }

  renderItem(item) {
    const name = this.state.byLid[item.split('/')[6]][0].fullname;
    const val = this.state.matchData.findIndex((el) => el.legislator === item);
    const matchPctPromise = ` %`;
    let pct;
    if (val === -1) {
      pct = ''
    } else {
      pct = this.state.matchData[0].pct;
    }
    return (
      <ListItem
        text={`Legislator: ${name} Match Pct: ${pct}`} // TODO add match percent
        success={this.success}
        setScrollEnabled={enable => this.setScrollEnabled(enable)}
      />
    );
    // }
  }

  updateLegislators = (val) => {
    this.setState((prevState) => {
      const updated = prevState.userInfo;
      updated.followed = [...prevState.followedLegislators, prevState.byLid[val][0].detail];

      AsyncStorage.setItem('user', JSON.stringify([updated]));
      console.log(prevState.followedLegislators, 'in updatelegislators');
      return {
        followedLegislators: [...prevState.followedLegislators, prevState.byLid[val][0].detail],
        pickerSelected: prevState.legislators[prevState.followedLegislators.length].detail.split('/')[6],
        addMode: false
      }
    }, this.updateFollowLegislators)
  };

  updateSelected = (val, index) => {
    this.setState({pickerSelected: val, leg: this.state.byLid[val]});
  };

  setMode = () => {
    const {legislators, followedLegislators} = this.state;

    const filtered = legislators.filter(function (item) {

      return followedLegislators.indexOf(item.detail) !== -1;
    });

    if (filtered.length || followedLegislators.length === 0) {
      this.setState({addMode: true})
    } else {
      console.log(this.state.followedLegislators);
      alert("All Legislators Already Selected")
    }
  };

  deleteLegislator = (rowData) => {
    this.setState((prevState) => {
      const updated = prevState.userInfo;
      console.log(rowData);
      const filtered = prevState.followedLegislators.filter(function (item) {
        return rowData !== item
      });

      updated.followed = [...filtered];
      console.log(filtered);
      AsyncStorage.setItem('user', JSON.stringify([updated]));
      console.log(prevState.followedLegislators, 'in updatelegislators');
      return {
        followedLegislators: [...filtered],
        pickerSelected: filtered[0].split('/')[6],
        addMode: false
      }
    }, this.updateFollowLegislators)
  };

  viewLegislator = (legislator) => {
    console.log(legislator, "in view legislator");

    this.props.navigation.navigate('LegislatorProfile', {"legislator": legislator, key: this.state.token});
  };

  renderRow(item) {
    const swipeBtns = [
      {
        text: 'Unfollow',
        backgroundColor: 'red',
        onPress: () => {
          this.deleteLegislator(item)
        }
      },
      {
        text: 'View Profile',
        backgroundColor: 'green',
        onPress: () => {
          this.viewLegislator(item)
        }
      }
    ];

    const name = this.state.byLid[item.split('/')[6]][0].fullname;
    const val = this.state.matchData.findIndex((m) => m.legislator === item);
    let pct;
    if (val === -1) {
      pct = ''
    } else {
      pct = this.state.matchData[0].match_percentage;
    }
    return (
      <Swipeout right={swipeBtns}
                autoClose={true}
                backgroundColor='transparent'>
        <TouchableHighlight
          // underlayColor='rgba(192,192,192,1,0.6)'
          onPress={(event) => this.viewLegislator(item)}>
          <View>
            <View>
              <Text> {`Legislator: ${name} Match Pct: ${pct}%`} </Text>
            </View>
          </View>
        </TouchableHighlight>
      </Swipeout>
    )
  }

  render() {
    const {navigate} = this.props.navigation;
    let {addMode, loading, legislators, pickerSelected, followedLegislators} = this.state;

    if (loading) {
      return <Boot/>
    }
    if (!addMode) {
      return (
        <View>
          <Image source={require('../../assets/topbanner_page4.png')}/>
          <View style={styles.titleText}>
            <Text style={styles.titleText}> Select politicians to Follow</Text>
            <TouchableHighlight onPress={this.setMode}>
              <Image source={require('../../assets/page4_empty_politician.png')}/>

            </TouchableHighlight>
          </View>
          <View>
            <FlatList
              style={this.props.style}
              data={this.state.followedLegislators}
              ItemSeparatorComponent={this.renderSeparator}
              renderItem={({item}) => this.renderRow(item)}
              scrollEnabled={this.state.enable}
            />

          </View>

        </View>
      )
    } else {
      return (

        <View style={{flex: 1}}>
          <Image source={require('../../assets/topbanner_page4.png')}/>
          <View>
            <SelectLegislators pickerSelected={pickerSelected} updateSelected={this.updateSelected}
                               legislators={legislators}
                               updateLegislators={this.updateLegislators}/>
          </View>
          <View>
            <FlatList
              style={this.props.style}
              data={this.state.followedLegislators}
              ItemSeparatorComponent={this.renderSeparator}
              renderItem={({item}) => this.renderRow(item)}
              scrollEnabled={this.state.enable}
            />
          </View>

        </View>

      )
    }
  }
}

const styles = StyleSheet.create({
  parent: {
    flex: 1
  },
  child: {
    flex: 2
  },
  listHalfView: {
    height: '50%'
  },
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
