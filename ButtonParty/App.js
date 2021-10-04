import { StatusBar } from 'expo-status-bar';
import React, { Component, useState } from 'react';
import { TouchableHighlight, StyleSheet, View, Text, Button } from 'react-native'
import AsyncStorage from '@react-native-async-storage/async-storage'

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
};

export default function App() {
  const [streak, setStreak] = useState('0');
  const [points, setPoints] = useState(0);

  const add = async () => {
    try {
      await AsyncStorage.setItem('streak', streak);
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
      AsyncStorage.clear();
    } catch(e) {
      console.log("Could not clear");
    }
  }

  const onPress = () => {
    try {
      getStreak();
      setStreak(JSON.stringify(parseInt(streak) + 1));
      let temp_streak = parseInt(streak);
      console.log(temp_streak);
      if(temp_streak <= 10) {
        setPoints(points + temp_streak);
      } else {
        setPoints(points + Math.pow(temp_streak, 2));
      }
      add();
    } catch (e) {
      console.log("crash");
    }
      
  }

  return (
    <View style = {styles.container}>
      <AppButton onPress={onPress} title="Button Party"/>
      <Text style={styles.bottomText}>Points: {points}</Text>
      <Text style={styles.bottomText}>Streak: {streak}</Text>
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
    width: 250,
    height: 250,
    borderRadius: 250,
    alignItems: 'center',
    justifyContent: 'center',
    elevation: 8,
  },
  appButtonText: {
    fontSize: 18,
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