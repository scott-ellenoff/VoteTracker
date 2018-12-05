# Milestone 5 #

# Installation Guide #

Requirements:

XCode 10.1
Homebrew v1.8.1
Node v8.11.3
NPM v6.4.1

1. Clone the git repository for front-end at:
https://github.com/scott-ellenoff/VoteTracker/tree/front-end

2. Ruby should be installed on your MacBook already. Install homebrew by running the following.
```python
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

3. Navigate to the folder at which you’ve downloaded the front-end project.

4. Run the following commands.
```python
brew install node
npm install 
```

5. Install React Native.
```python
npm install -g react-native-cli
```

6. Set command line tools by opening XCode application. 

7. Resolve compabitility issue between XCode10 and React client. Navigate to your project root, and run these. 
```python
$ cd node_modules/react-native/scripts && ./ios-install-third-party.sh && cd ../../../
$ cd node_modules/react-native/third-party/glog-0.3.5/ && ../../scripts/ios-configure-glog.sh && cd ../../../../
```

8. Upgrade react-native to catch older versions, and link. 
```python
react-native upgrade
react-native link
```

9. Run for iOS now. The simulator should load, and the VoteTracker app should start up automatically, with "Build Success" showing in Terminal. Otherwise we will see "Build Failed".  
```python
react-native run-ios
```

If you get any errors or have any trouble please reach out to Zach Kamran and/or Yasoob Rasheed facebook or by email (kamranzach@uchicago.edu, yasoobr@uchicago.edu). 

# Functionality #
The main idea of this app is that users can vote on the same bills that our House and Senate representatives vote on and see how much they align with a particular legislators.
In particular we provide an interface in the home page for users to vote on new bills currently ont he house and senate floor. Once the real vote happens the user can view a map of how legislators voted and in their profile page users can see how their votes matched with legislators they follow.
In addition they can see all of their past votes in the home page.  
# Usage Guide #
To use the app follow the installation instructions above. Once the App is running create a login by clicking "Sign Up". You can then use this to login and "Start Tracking the Votes". 

