'use strict'



import Home from './components/Home.js'
import Main from './components/Main.js'
import Profile from './components/Profile/Profile.js'

import {
    createStackNavigator,
} from 'react-navigation'

const App = createStackNavigator(
    {
        Home: {screen: Home},
        Main: {screen: Main},
        Profile: {screen: Profile}
    }
);

export default App;
