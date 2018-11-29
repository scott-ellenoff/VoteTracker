import React, {Component} from 'react';
import {View, Text, Picker, StyleSheet, Button} from 'react-native'

export default class SelectLegislators extends Component {
  state = {
  };

  handleConfirmClick = () => {
    this.props.updateLegislators(this.props.pickerSelected);
  };


  render() {

    const {legislators} = this.props;
    console.log(legislators, 'here');
    return (
      <View>
        <Button onPress={this.handleConfirmClick} title={"Add"}/>
        <Picker selectedValue={this.props.pickerSelected}
                onValueChange={(itemValue, itemIndex) => this.props.updateSelected(itemValue, itemIndex)}>
          {legislators.map((val, i) => <Picker.Item label={val.fullname} value={val.LID} key={i}/>)}
        </Picker>
      </View>
    )
  }
}

const styles = StyleSheet.create({
  text: {
    fontSize: 30,
    alignSelf: 'center',
    color: 'red'
  }
})
