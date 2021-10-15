import { StatusBar } from 'expo-status-bar';
import React, { useState } from 'react';
import { TouchableHighlight, StyleSheet, View, Text, Button } from 'react-native'
import AsyncStorage from '@react-native-async-storage/async-storage'

export default function App() {
  //Setting up hook variables for streak and points
  let [streak, setStreak] = useState(0);
  let [points, setPoints] = useState(0);
  let username = "bdngeorge";

  // //Sets the streak key in local storage to current streak value after button press
  // const set = async (val) => {
  //   try {
  //     await AsyncStorage.setItem('streak', val);
  //   } catch (e) {
  //     console.log("Unable to save data");
  //   }
  // }

  // //Fetches the current streak value
  // //Sets variable "streak" to stored val
  // const getStreak = async () => {
  //   try {
  //     const val = await AsyncStorage.getItem('streak');
  //     if(val != null) {
  //       setStreak(val);
  //     } 
  //   } catch (e) {
  //     console.log("Unable to read streak data");
  //   }
  // }

  //Clears the stored data, added this for testing 
  //also could be used if user deletes account
  const clear = async () => {
    try {
      await AsyncStorage.clear();
      setStreak('0');
    } catch(e) {
      console.log("Could not clear");
    }
  }

  //Called when button is pressed, handles points increment
  const onPress = async () => {
    var obj;
    try {
      await fetch('https://qrtybatu2l.execute-api.us-east-1.amazonaws.com/press?body=' + username);
      await fetch('https://qrtybatu2l.execute-api.us-east-1.amazonaws.com/fetch/self?username=' + username)
        .then(res => res.json())
        .then(data => obj = data)
        .then(() => console.log(obj));

      setPoints(obj['score']);
      setStreak(obj['streak']);
    } catch (error) {
      console.log(error);
    }
  }

  //Custom button component
  const AppButton = ({ onPress, title }) => {
    return (
      <TouchableHighlight 
        activeOpacity={.8}
        underlayColor="#db0000"
        onPress={onPress}
        style={styles.appButtonContainer}
      >
        <Text style={styles.appButtonText}>{title}</Text>
      </TouchableHighlight>
    );
  }

  return (
    <View style = {styles.container}>
      <Text style={styles.topText}>
        <Text style={styles.points}>Points: {points}</Text>
        <Text style={styles.streak}>Streak: {streak}</Text>
      </Text>
      <AppButton onPress={onPress} title="Button Party"/>
      <Button style={styles.buttomButton} onPress={clear} title="Clear"/>
      <Button style={styles.buttomButton} onPress={() => setPoints(0)} title="Reset Points"/>
    </View>
);
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#c2c2c2',
    alignItems: 'center',
    justifyContent:'space-evenly'
  },
  appButtonContainer: {
    backgroundColor: '#ff0000',
    width: 350,
    height: 350,
    borderRadius: 390,
    alignItems: 'center',
    justifyContent: 'center',
    elevation: 8,
  },
  appButtonText: {
    fontSize: 30,
    color: '#000',
    fontWeight: 'bold',
    alignSelf: 'center',
    textTransform: 'uppercase'
  },
  topText: {
    paddingTop: 50,
    fontSize: 18,
    color: '#000',
    flexDirection: 'row',
    fontWeight: 'bold',
    textTransform: 'uppercase',
    justifyContent:'space-between'
  },
});