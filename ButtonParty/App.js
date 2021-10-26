import { StatusBar } from 'expo-status-bar';
import React, { useState, useEffect } from 'react';
import { TouchableHighlight, ImageBackground, StyleSheet, View, Text, Button, Alert } from 'react-native'
import AsyncStorage from '@react-native-async-storage/async-storage'
import messaging from '@react-native-firebase/messaging';

export default function App() {
  //Setting up hook variables for streak and points
  let [streak, setStreak] = useState(0);
  let [points, setPoints] = useState(0);
  let username = "bdngeorge";

  useEffect(() => {
    console.log(messaging().getToken());

    const unsubscribe = messaging().onMessage(async remoteMessage => {
      Alert.alert('A new FCM message arrived!', JSON.stringify(remoteMessage));
    });

    return unsubscribe;
  }, []);



  //Clears the stored data, added this for testing 
  //also could be used if user deletes account
  const clear = async () => {
    try {
      await AsyncStorage.clear();
      setStreak(0);
      setPoints(0);
    } catch(e) {
      console.log("Could not clear");
    }
  }

  //Called when button is pressed, handles points increment
  const onPress = async () => {
    messaging().getToken().then(rtrn => console.log(rtrn));
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
    <View style={styles.container}>
      <View style={styles.topText}>
        <Text style={styles.Title}>BUTTON PARTY</Text>
        <Text style={styles.Scores}>
          <Text style={styles.points}>Points: {points}                                                </Text>
          <Text style={styles.streak}>Streak: {streak}</Text>
        </Text>
      </View>
      <View style={styles.button}>
        <AppButton onPress={onPress} title=""/>
      </View>
      <View style={styles.tempButtons}>
        <Button style={styles.buttomButton} onPress={clear} title="Clear"/>
        <Button style={styles.buttomButton} onPress={() => setPoints(0)} title="Reset Points"/>
      </View>
    </View>
);
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    backgroundColor: '#c2c2c2',
    justifyContent: 'space-between'
  },
  topText: {
    flex: .15,
    alignItems: 'center',
    textTransform: 'uppercase',
  },
  Title: {
    fontSize: 30,
    color: '#000',
    fontWeight: 'bold',
  },
  Scores: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#000',
  },
  button: {
    flex: .55,
  },
  tempButtons: {
    flex: .3,
  },
  appButtonContainer: {
    backgroundColor: '#ff0000',
    width: 350,
    height: 350,
    borderRadius: 390,
    alignItems: 'center',
    justifyContent: 'center',
    elevation: 10,
  },
  appButtonText: {
    fontSize: 30,
    color: '#000',
    fontWeight: 'bold',
    alignSelf: 'center',
    textTransform: 'uppercase'
  },
});