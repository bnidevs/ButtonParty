import React, { useState, useEffect } from 'react';
import { TouchableHighlight, ImageBackground, StyleSheet, View, Text, Button, Alert } from 'react-native'
import AsyncStorage from '@react-native-async-storage/async-storage'
import messaging from '@react-native-firebase/messaging';
import notifee, { EventType } from '@notifee/react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

/*************************\
    GLOBAL FUNCTIONS
\*************************/
const Stack = createNativeStackNavigator();

//oauth packages
import auth from '@react-native-firebase/auth';
import {
  GoogleSignin,
  GoogleSigninButton,
  statusCodes,
} from '@react-native-google-signin/google-signin';


GoogleSignin.configure({
  webClientId:
    '582017907775-cmhpth94hvbpj3fkh8jd847ig8omjr2a.apps.googleusercontent.com',
  offlineAccess: true
});

/*************************\
       APP FUNCTIONS
\*************************/
export default function App() {
  //Setting up hook variables for streak and points
  let [streak, setStreak] = useState(0);
  let [points, setPoints] = useState(0);
  let [active, setActive] = useState(false);
  let [username, setUsername] = useState("");
  let usernameTmp = "bdngeorge";


  /*************************\
    NOTIFICATION FUNCTIONS
  \*************************/
  async function onMessageReceived(message) {
    // Create a channel
    const channelId = await notifee.createChannel({
      id: 'default',
      name: 'Default Channel',
    });

    // Display a notification
    await notifee.displayNotification({
      title: '<p style="color:red;"><b>Press the Button</b></p>',
      body: '<em>You have 1 minute to press the button!</em>',
      android: {
        channelId : 'default',
          autoCancel : true,
          pressAction: {
              id: "default",
          },
      }
    });
  }
  notifee.onBackgroundEvent(async ({ type, detail }) => {
    if (type === EventType.PRESS) {
      console.log('User pressed the notification.', detail.pressAction.id);
    }
  });
  useEffect(() => {
    const foreground = messaging().onMessage(async remoteMessage => {
      console.log('A new FCM message arrived!', JSON.stringify(remoteMessage['data']['message']));
      onMessageReceived(remoteMessage);
      setActive(true);
      setTimeout(() => { setActive(false); }, 60000);
    });

    return foreground;
  }, []);
  useEffect(() => {
    const background = messaging().setBackgroundMessageHandler(async remoteMessage => {
      console.log('Message handled in the background!', JSON.stringify(remoteMessage['data']['message']));
      onMessageReceived(remoteMessage);
      setActive(true);
      setTimeout(() => { setActive(false); }, 60000);
    });

    return background;
  }, []);


  /*************************\
    GOOGLE OAUTH FUNCTIONS
  \*************************/
  const signIn = async () => {
    try {
      await GoogleSignin.hasPlayServices();

      GoogleSignin.signIn().then(
        userInfo => {
          setUsername(userInfo['user']['id']);
          console.log(userInfo);
        },
        error=>{
          console.log(username);
          console.log(error);
        }
      );
      //this.setState({ userInfo });

      
      
    } catch (error) {
      if (error.code === statusCodes.SIGN_IN_CANCELLED) {
        // user cancelled the login flow
        console.log("CANCELLED")
      } else if (error.code === statusCodes.IN_PROGRESS) {
        // operation (e.g. sign in) is in progress already
        console.log("IN-PROGRESS")
      } else if (error.code === statusCodes.PLAY_SERVICES_NOT_AVAILABLE) {
        // play services not available or outdated
        console.log('PLAY-SERVICES-NOT-AVAILABLE')
      } else {
        // some other error happened
        console.log("OTHER ERROR")
      }
      
    }
  };


  /*************************\
      BUTTON FUNCTIONS
  \*************************/
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
        style={[styles.button, active ? styles.enabled : styles.disabled]}
      >
        <Text style={styles.appButtonText}>{title}</Text>
      </TouchableHighlight>
    );
  }

  /*************************\
    SCREEN FUNCTIONS
  \*************************/
  const button_screen = ({navigation}) => {
    return (
      <View style={styles.buttonContainer}>
        <View style={styles.topText}>
          <Text style={styles.Title}>BUTTON PARTY</Text>
          <Text style={styles.Scores}>
            <Text style={styles.points}>Points: {points}                                                </Text>
            <Text style={styles.streak}>Streak: {streak}</Text>
          </Text>
        </View>
        <View style={styles.button}>
          <AppButton onPress={onPress} title="The Button"/>
        </View>
        <View style={styles.tempButtons}>
          <Button style={styles.buttomButton} onPress={() => setStreak(0)} title="Clear"/>
          <Button style={styles.buttomButton} onPress={() => setPoints(0)} title="Reset Points"/>
          <Button style={styles.buttomButtom} onPress={() => setActive(!active)} title="Button ON/OFF"/>
          <Button title="Display Notification" onPress={() => onMessageReceived()} />
          <Button
            title="Switch Screens"
            onPress={() => 
              navigation.navigate('Test')
            }
          />
        </View>
        <Text>Active: {active ? "true" : "false"}</Text>
      </View>
    );
  }

  const signIn_screen = ({navigation}) => {
    return (
      <View style={styles.signinContainer}>
        <Text style={styles.topText, styles.Title}>Sign In</Text>
        <Button
          title="Return to button"
          onPress={() => 
            navigation.navigate('Button')
          }
        />

        <GoogleSigninButton
          style={{ width: 192, height: 48 }}
          size={GoogleSigninButton.Size.Wide}
          color={GoogleSigninButton.Color.Dark}
          onPress={signIn}
        />
      </View>
    );
  }

  /*************************\
            RETURN 
  \*************************/
  return (
    <NavigationContainer>
      <Stack.Navigator>             
        <Stack.Screen name="Test" component={signIn_screen} options={{ headerShown: false}} />      
        <Stack.Screen name="Button" component={button_screen} options={{ headerShown: false}} />   
      </Stack.Navigator>
    </NavigationContainer>
  );
}

/*************************\
          STYLES
\*************************/
const styles = StyleSheet.create({
  buttonContainer: {
    flex: 1,
    alignItems: 'center',
    backgroundColor: '#c2c2c2',
    justifyContent: 'space-between'
  },
  signinContainer: {
    flex: 1,
    alignItems: 'center',
    backgroundColor: '#c2c2c2',
    justifyContent: 'space-evenly'
  },
  topText: {
    flex: .15,
    alignItems: 'center',
    top: 0,
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
  button: {
    width: 350,
    height: 350,
    borderRadius: 390,
    alignItems: 'center',
    justifyContent: 'center',
    elevation: 10,
  },
  enabled: {
    backgroundColor: '#ff0000',
  },
  disabled: {
    backgroundColor: '#db0000',
  },
  appButtonText: {
    fontSize: 30,
    color: '#000',
    fontWeight: 'bold',
    alignSelf: 'center',
    textTransform: 'uppercase'
  },
});