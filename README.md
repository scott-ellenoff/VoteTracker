# Milestone 4b #

# How To Compile Front-End #

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

This will take a bit of time, so hang on. If you still get a CFBundleIdentifier error, please contact yasoobr@uchicago.edu, as this is a compatibility problem with XCode and React Native. 

# Sample Login Credentials #
--Set1--
Username: scottwang4
Password: uchicago4

--Set2--
Username: scottwang0
Password: uchicago0

# How to Run Back-End #

Our back-end is deployed on a separate server and does not need to be launched locally to test. For the instructions on how to run the unit tests please see the section below.

# How to Run Unit Cases (Acceptance Test Examples) #

First, install all necessary dependencies by running:

```
pip install -r requirements.txt
```
To run the unit tests for the backend API run:
```
cd src/backend
python manage.py test
```
This will create a test database and run our unit tests.

We have written tests for:
* Matching algorithm
* Push notifications (tests were written, but the functionality was not implemented for the reasons described below)
* Updating the bill/votes database
* User login

We have chosen to write tests for the above using python's unittest library. Testing connection of frontend and backend also is done through our existing tests that call the Django API.

# What Has Been Implemented #
**Front-End:** <br />

**Back-End:** <br />
For the second iteration, we plan to connect the backend to the front-end and add new features. More specifically, we want to execute on the Django REST API and AWS server we’ve built and actually integrate response/requests into our front-end code. We are going to finish the user login portion, develop push notifications, update the bill and voting information, develop a matching algorithm, and finally develop the map. This seems like a lot, but we’ve split up the tasks well.

# Who Did What? #

**Emily Xue**: 
* Please put text here

**Hasmik Grigoryan**:
* Visualizing how the United States senators have voted on a specific bill
  
**Larry Chen**: 
* Worked on setting up a registration form, login/logout endpoint, and adding permissions to certain endpoints so that only authenticated users can access their user information; <br />
* Launched an Amazon EC2 instance and deploying the django backend server in production mode <br />
  
**Scott Ellenoff**:
* Worked on connecting front and backend, as well as creating the matching algorithm to match Users and Legislators <br />

**Scott Wang**: 
* Implemented and tested login auth from front-end;
* Created, implemented and tested a sign up screen/auth navigable from the login screen, also from front-end.

**Stepan Severov**:
* Worked on populating the database with previous legislator votes;
* Wrote the scripts that automatically push new bills and votes to the database as soon as they come out, deploying the script on the server to run as a cronjob; 
* Modified the unit tests in accordance with the feedback to milestone 4a and the inner refactoring.

**Yasoob Rasheed**:
* Connected front and back-end, generalizing data in component state, to pass it from View Controller to View Controller in the front-end application;
* Worked on sending bill information to the Main page so that Users can vote and see their history.

**Zach Kamran**:
* Worked on Login and Signup page on front-end
* Changed the legislators that users follow in profile page.

# Have We Made Any Changes? #

We were not able to implement push-notifications as planned because doing so requires an Apple Developer account which costs $99 per year and it takes Apple up to two weeks to verify you as a developer. <br />

PullLegislatorVotes() functionality that was planned to be implemented inside the Bill class, now will be running as a cron process on the server side due to that being easier, considering we are using an external ProPublica API to pull records on any new votes which were made public. After obtaining those votes, we update the Votes table described above, recording the legislators’ voting decisions. <br />

# Anything You'd Like the TA to Know #

