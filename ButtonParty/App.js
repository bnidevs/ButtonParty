import { StatusBar } from 'expo-status-bar';
import React, { useState, useEffect } from 'react';
import { TouchableHighlight, ImageBackground, StyleSheet, View, Text, Button, Alert } from 'react-native'
import AsyncStorage from '@react-native-async-storage/async-storage'
import messaging from '@react-native-firebase/messaging';
import {Authentication, Authenticated} from 'screens'

//oauth packages
import auth from '@react-native-firebase/auth';
import { GoogleSignin } from '@react-native-community/google-signin';

GoogleSignin.configure({
  webClientId:
    '260759292128-4h94uja4bu3ad9ci5qqagubi6k1m0jfv.apps.googleusercontent.com',
});


export default function App() {
  //Setting up hook variables for streak and points
  let [streak, setStreak] = useState(0);
  let [points, setPoints] = useState(0);
  let [active, setActive] = useState(false);
  let username = "bdngeorge";

  useEffect(() => {
    const foreground = messaging().onMessage(async remoteMessage => {
      console.log('A new FCM message arrived!', JSON.stringify(remoteMessage['data']['message']));
      setActive(true);
    });

    return foreground;
  }, []);
  useEffect(() => {
    const background = messaging().setBackgroundMessageHandler(async remoteMessage => {
      console.log('Message handled in the background!', JSON.stringify(remoteMessage['data']['message']));
      setActive(true);
    });

    return background;
  }, []);

  //Called when button is pressed, handles points increment
  const onPress = async () => {
    setActive(false);
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
        disabled = {!active}
        activeOpacity={.8}
        underlayColor="#db0000"
        onPress={onPress}
        style={active ? styles.enabled : styles.disabled}
      >
        <Text style={styles.appButtonText}>{active ? title : "Disabled"}</Text>
      </TouchableHighlight>
    );
  }

  const [authenticated, setAuthenticated] = useState(false);

  useEffect(() => {
    GoogleSignin.configure({
      webClientId:
       '582017907775-cmhpth94hvbpj3fkh8jd847ig8omjr2a.apps.googleusercontent.com',
    });
  }, []);

  async function onGoogleButtonPress() {
    // Get the users ID token
    const { idToken } = await GoogleSignin.signIn();

    // Create a Google credential with the token
    const googleCredential = auth.GoogleAuthProvider.credential(idToken);

    // Sign-in the user with the credential
    return auth().signInWithCredential(googleCredential);
  }
  auth().onAuthStateChanged((user) => {
    if (user) {
      setAuthenticated(true);
    } else {
      setAuthenticated(false);
    }
  });

  if (authenticated) {
    return <Authenticated />;
  }

  return <Authentication onGoogleButtonPress={onGoogleButtonPress} />;



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
        <AppButton onPress={onPress} title="Press"/>
      </View>
      <View style={styles.tempButtons}>
        <Button style={styles.buttomButton} onPress={() => setStreak(0)} title="Clear"/>
        <Button style={styles.buttomButton} onPress={() => setPoints(0)} title="Reset Points"/>
        <Button style={styles.buttomButtom} onPress={() => setActive(!active)} title="Button ON/OFF"/>
      </View>
      <Text>Active: {active ? "true" : "false"}</Text>
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
  enabled: {
    backgroundColor: '#ff0000',
    width: 350,
    height: 350,
    borderRadius: 390,
    alignItems: 'center',
    justifyContent: 'center',
    elevation: 10,
  },
  disabled: {
    backgroundColor: '#db0000',
    width: 350,
    height: 350,
    borderRadius: 390,
    alignItems: 'center',
    justifyContent: 'center',
    elevation: 10,
  },
  appButtonContainer: {
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