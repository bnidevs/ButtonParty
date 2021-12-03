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
  let [navigation, setNavigation] = useState("login");
  let usernameTmp = "bdngeorge";

  /*************************\
     USE EFFECT FUNCTIONS
  \*************************/
  useEffect(() => {
    AsyncStorage.getItem('username')
      .then(val => {
        if(val != null) {
          setUsername(val);
          setNavigation('button');
          fetch('https://qrtybatu2l.execute-api.us-east-1.amazonaws.com/fetch/self?username=' + val)
            .then(res => res.json())
            .then(data => {
              setPoints(data['score']);
              setStreak(data['streak']);
            });
        }
      },
      error=>console.log(error));
    }, []);

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
      buttonActive();
    });

    return foreground;
  }, []);
  useEffect(() => {
    const background = messaging().setBackgroundMessageHandler(async remoteMessage => {
      console.log('Message handled in the background!', JSON.stringify(remoteMessage['data']['message']));
      onMessageReceived(remoteMessage);
      buttonActive();
    });

    return background;
  }, []);


  /*************************\
    GOOGLE OAUTH FUNCTIONS
  \*************************/
  const signIn = async () => {
    try {
      await GoogleSignin.hasPlayServices();
      const mToken = await messaging().getToken()
      console.log(mToken);

      GoogleSignin.signIn().then(
        userInfo => {
          setUsername(userInfo['user']['id']);
          fetch('https://qrtybatu2l.execute-api.us-east-1.amazonaws.com/add', {
            method: "POST",
            body: JSON.stringify({
              "RequestBody": {
                "username": userInfo['user']['id'],
                "token": mToken
              }
            })
          });

          fetch('https://qrtybatu2l.execute-api.us-east-1.amazonaws.com/fetch/self?username=' + userInfo['user']['id'])
            .then(res => res.json())
            .then(data => {
              setPoints(data['score']);
              setStreak(data['streak']);
            });
          setNavigation('button');

          AsyncStorage.setItem('username', '' + userInfo['user']['id']);

        
        },
        error=>{
          console.log(username);
          console.log(error);
        }

        
      );

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
  function buttonActive() {
    setActive(true);
    setTimeout(() => { setActive(false); }, 100000);
  }


  const onPress = async () => {
    setActive(false);
    messaging().getToken().then(rtrn => console.log(rtrn));
    try {
      await fetch('https://qrtybatu2l.execute-api.us-east-1.amazonaws.com/press', {
        method: "POST",
        body: JSON.stringify({
          "RequestBody": {
            "username": username,
          }
        })
      });
      await fetch('https://qrtybatu2l.execute-api.us-east-1.amazonaws.com/fetch/self?username=' + username)
        .then(res => res.json())
        .then(data => {
          setPoints(data['score']);
          setStreak(data['streak']);
        });
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
        style={[buttonStyle.button, active ? buttonStyle.enabled : buttonStyle.disabled]}
      >
        <Text></Text> 
      </TouchableHighlight>
    );
  }

  /*************************\
    SCREEN FUNCTIONS
  \*************************/
  const button_screen = () => {
    return (
      <View style={{ flex: 1, backgroundColor: '#363636'}}>
        <View style={{ flex: 1}}>
          <Text style={home.title}>BUTTON PARTY</Text>
          <View style={{flexDirection: 'row', justifyContent: 'space-between'}}>
            <Text style={home.scoreText}>Points: {points}</Text>
            <Text style={home.scoreText}>Streak: {streak}</Text>
          </View>
          <View style={{flexDirection: 'row-reverse'}}>
            <TouchableHighlight 
              activeOpacity={.8}
              underlayColor="#db0000"
              onPress={() => setNavigation('Inventory')}
              style={home.shop}
            >
              <Text style={{fontWeight: 'bold', color: 'white'}}>SHOP</Text>
            </TouchableHighlight>
          </View>
        </View>

        <View style={{ flex: 2.5, justifyContent: 'center'}}>
          <AppButton onPress={onPress}/>
        </View>

        <View style={{ flex: 1, flexDirection: 'column-reverse', alignItems: 'center' }}>
           <Text style={{fontWeight: 'bold', color: 'grey', fontSize: 10}}>Trademark?</Text>
        </View>
      </View>
    );
  }

  const signIn_screen = () => {
    return (
      <View style={{flex: 1, backgroundColor: '#363636'}}>
        <View style={{flex:1, flexDirection: 'column-reverse'}}>
         <Text style={home.title}>ButtonParty</Text>
        </View>

        <View style={{flex:2, alignItems: 'center', justifyContent: 'center'}}>
          <GoogleSigninButton
            style={{width: 192, height: 48 }}
            size={GoogleSigninButton.Size.Wide}
            color={GoogleSigninButton.Color.Light}
            onPress={signIn}
          />
        </View>
      </View>
    );
  }

  /*************************\
            RETURN 
  \*************************/
  return (
    <NavigationContainer>
      <Stack.Navigator>             
        {
          navigation == 'login' ?
          <Stack.Screen name="Login" component={signIn_screen} options={{ headerShown: false}} /> :
          <Stack.Screen name="Button" component={button_screen} options={{ headerShown: false}} />
        }   
      </Stack.Navigator>
    </NavigationContainer>
  );
}

/*************************\
          STYLES
\*************************/
const home = StyleSheet.create({
  title: {
    fontSize: 30,
    fontWeight: 'bold',
    color: 'white',
    alignSelf: 'center',
    paddingBottom: 15
  },
  scoreText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: 'white',
    padding: 5
  },
  shop: {
    backgroundColor: '#ff0000',
    width: 75,
    height: 75,
    borderRadius: 75,
    alignItems: 'center',
    justifyContent: 'center',
  }
});

const buttonStyle = StyleSheet.create({
  button: {
    alignSelf: 'center',
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
    backgroundColor: '#910000',
  },
});
