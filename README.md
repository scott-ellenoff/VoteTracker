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

# Design Review #
See other document. DesignReview.pdf. 
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
* Built major components of the front-end and worked closely with the back-end team to connect REST endpoints to frontend. 
* In particular built the Profile page and Legislator Profile page including add legislator functionality
* Worked on Login and Signup page on front-end;
* Worked on React Framework (Profile, Segues);
* Built major components of the front end and connected the front-end and backend. 
* Worked closely with back-end team to address and fix bugs found in acceptance testing




# Anything You'd Like the TA to Know #

