import React, {Component} from 'react';
import {View, Text, Picker, StyleSheet, Button} from 'react-native'

export default class SelectLegislators extends Component {
  state = {
    pickerSelected: 'Steve',
    availableLegislators: [{label: "Steve", value: "steve"}, {label: "Ellen", value: "ellen"}, {
      label: "Maria",
      value: "maria"
    }]
  };
  updateSelected = (val) => {
    console.log(val);
    this.setState({pickerSelected: val})
  };

  handleConfirmClick = () =>  {
    console.log(this.state.pickerSelected, 'jklfad');
    this.props.updateLegislators(this.state.pickerSelected);

    this.setState((prevState) => {
      return {availableLegislators: [...prevState.availableLegislators]}
    });
  }

  render() {
    const {availableLegislators} = this.state;
    return (
      <View>
        <Picker selectedValue={this.state.pickerSelected} onValueChange={this.updateSelected}>
          {availableLegislators.map((val, i) => <Picker.Item label={val.label} value={val.label} key={i}/>)}
        </Picker>
        <Button onPress={this.handleConfirmClick} title={"Add"}/>
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
