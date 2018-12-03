# Milestone 4b #

# Installation Guide#

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
9. Open the proect in xCode by opening the VoteTracker.xcodeproj file in the ios folder of frontend. Navigate to the build settings tab in xCode. Change the Framework search path in xCode BuildSettings tab to the path for the ios folder on your computer. I.e my framework search path is  /Users/zachkamran/WebstormProjects/VoteTracker/src/frontend/ios.

10. Run for iOS now. The simulator should load, and the VoteTracker app should start up automatically, with "Build Success" showing in Terminal. Otherwise we will see "Build Failed".  
```python
react-native run-ios
```

This will take a bit of time, so hang on. If you still get a CFBundleIdentifier error, please contact yasoobr@uchicago.edu, as this is a compatibility problem with XCode and React Native. 

# Functionality #

# Usage Guide #

# Design Review #

We have implemented the core functionalities that we proposed. This includes being able to vote on bills, view bill descriptions, compare one's voting history with those of other senators via a match percentage, login and authentication, and data visualization of senator votes. In terms of functionality that was proposed but not implemented, we did not provide the APIs needed for those who want to get data about votes and legislators. 

# Contributions #

**Emily Xue**: 
* Wrote updated Django views that control HTTP requests to the endpoints
* Wrote/updated tests, including authorization tests

**Hasmik Grigoryan**:
* Visualizing how the United States senators have voted on a specific bill.
  
**Larry Chen**: 
* Worked on setting up a registration form, login/logout endpoint, and adding permissions to certain endpoints so that only authenticated users can access their user information; <br />
* Launched an Amazon EC2 instance and deploying the django backend server in production mode. <br />
  
**Scott Ellenoff**:
* Worked on connecting front and backend, as well as creating the matching algorithm to match Users and Legislators. <br />

**Scott Wang**: 
* Implemented and tested login auth from front-end;
* Created, implemented and tested a sign up screen/auth navigable from the login screen, also from front-end.

**Stepan Severov**:
* Worked on populating the database with previous legislator votes;
* Wrote the scripts that automatically push new bills and votes to the database as soon as they come out, deploying the script on the server to run as a cronjob; 
* Worked on the readme

**Yasoob Rasheed**:
* Connected front and back-end, generalizing data in component state, to pass it from View Controller to View Controller in the front-end application;
* Worked on sending bill information to the Main page so that Users can vote and see their history.

**Zach Kamran**:
* Worked on Login and Signup page on front-end;
* Changed the legislators that users follow in profile page;
* Built Profile page allowing users to follow legislators and see match percentage.


# Anything You'd Like the TA to Know #

