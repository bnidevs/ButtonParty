import { StatusBar } from 'expo-status-bar';
import React, { Component, useState, useEffect } from 'react';
import { TouchableHighlight, StyleSheet, View, Text, Button } from 'react-native'
import AsyncStorage from '@react-native-async-storage/async-storage'

export default function App() {

  let [streak, setStreak] = useState('0');
  let [points, setPoints] = useState(0);

  const set = async (val) => {
    try {
      await AsyncStorage.setItem('streak', val);
    } catch (e) {
      console.log("Unable to save data");
    }
  }

  const getStreak = async () => {
    try {
      const val = await AsyncStorage.getItem('streak');
      if(val != null) {
        setStreak(val);
      } 
    } catch (e) {
      console.log("Unable to read streak data");
    }
  }

  const clear = async () => {
    try {
      await AsyncStorage.clear();
      setStreak('0');
    } catch(e) {
      console.log("Could not clear");
    }
  }

  function onPress() {
    getStreak();
    let temp_streak = parseInt(streak) + 1;
    if(temp_streak <= 10) {
      setPoints(points + temp_streak);
    } else {
      setPoints(points + Math.pow(temp_streak, 2));
    }
    set(temp_streak.toString());   
  }

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


  getStreak();
  return (
    <View style = {styles.container}>
      <AppButton onPress={onPress} title="Button Party"/>
      <Text style={styles.bottomText}>Points: {points}</Text>
      <Text style={styles.bottomText}>Streak: {streak}</Text>
      <Button onPress={clear} title="Clear"/>
    </View>
);
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#c2c2c2',
    alignItems: 'center',
    justifyContent: 'center',
  },
  appButtonContainer: {
    backgroundColor: "#ff0000",
    width: 390,
    height: 390,
    borderRadius: 390,
    alignItems: 'center',
    justifyContent: 'center',
    elevation: 8,
  },
  appButtonText: {
    fontSize: 30,
    color: "#000",
    fontWeight: "bold",
    alignSelf: "center",
    textTransform: "uppercase"
  },
  bottomText: {
    paddingTop: 50,
    fontSize: 18,
    color: "#000",
    fontWeight: "bold",
    alignSelf: "center",
    textTransform: "uppercase"
  },
  clear: {
    
  }
});