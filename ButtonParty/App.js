import { StatusBar } from 'expo-status-bar';
import React, {useState} from 'react';
import { TouchableHighlight, StyleSheet, View, Text, Button } from 'react-native'

const AppButton = ({ onPress, title }) => (
  <TouchableHighlight 
    activeOpacity={.8}
    underlayColor="#db0000"
    onPress={onPress} 
    style={styles.appButtonContainer}
  >
    <Text style={styles.appButtonText}>{title}</Text>
  </TouchableHighlight>
);

const App = () => {
  const [points, setPoints] = useState(0);
  const onPress = () => (
    
    setPoints(prevCount => prevCount + 1)
  );

  return (
    <View style = {styles.container}>
      <AppButton onPress = {onPress} title="Button Party"/>
      <Text style={styles.points}>Points: {points}</Text>
    </View>
 )
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
  points: {
    paddingTop: 50,
    fontSize: 18,
    color: "#000",
    fontWeight: "bold",
    alignSelf: "center",
    textTransform: "uppercase"
  }
});


export default App