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

For acceptance test, please feel free to use our app (register, login, vote on bills, view the bill info, modify your profile, follow some legislators, view maps). It can be done by following the instructions for the front-end tests, or **Yasoob** can help you to get it running on your phone to get the full experience.

# What Has Been Implemented #
For the second iteration, we have successfully connected the backend to the front-end and added some new features. <br /> 

**Front-End:** <br />
* We have created three main pages: login, home, and profile.
* Login page lets the user to either access their account or create a new one.
* The main page allows users to vote and see the bills for which they have not yet expressed their opinion. Each bill object is clickable and contains information about that bill as well as the map, which shows how the legislators voted on(one map per bill).
* The profile screen allows the user to follow any legislator and see how well these legislators matched user’s votes.

**Back-End:** <br />
* We executed on the Django REST API and AWS server we’ve built and actually integrated response/requests into our front-end code;
* We have finished the user login and registration parts, having all the user credentials stored in our database;
* We have also set up our database to use authentication, ensuring only authorized admins can manually access and modify it. Users’ actions in the database are limited to viewing/editing their own information, as well as seeing the voting history for them and the legislators. We have also put in basic methods to prevent data corruption and duplicate occurrence in the database;
* We have implemented the logic for following and matching the legislators. Now each user has a list of followed legislators in their database entry. In addition to the Bills, Votes, Legislators, and Users tables we already had, we have also added the Matches table that stores the match percentages between the users and the legislators they follow. Each entry in the User table has a list of links to the entries in the Matches table (please see the db_schema.pdf for more info);
* Each User now also has a list of unvoted bills for which they have not yet expressed their opinion. Once the user votes on such bill, the bill is removed from the unvoted list, a new vote entry is created in the Votes table, and the matching percentage is updated for the legislators the user is following;
* We have set up an automatic updater (cronjob) that runs on the server side and updates the database as soon as new bills or votes come out. We do not record all the bills to our database, but only those that we find relevant for our project and socially controversial;
* We have also generated maps for each bill, showing how legislators in each district voted on that bill.

# Who Did What? #

**Emily Xue**: 
* Please put text here

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
* Modified the unit tests in accordance with the feedback to milestone 4a and the inner refactoring.

**Yasoob Rasheed**:
* Connected front and back-end, generalizing data in component state, to pass it from View Controller to View Controller in the front-end application;
* Worked on sending bill information to the Main page so that Users can vote and see their history.

**Zach Kamran**:
* Worked on Login and Signup page on front-end;
* Changed the legislators that users follow in profile page;
* Built Profile page allowing users to follow legislators and see match percentage.

# Have We Made Any Changes? #

Overall, we believe that we have followed our plan for this milestone closely. However, there were some minor logistical changes that we had to make: <br />

We were not able to implement push-notifications as planned because doing so requires an Apple Developer account which costs $99 per year and it takes Apple up to two weeks to verify you as a developer. <br />

We have added additional tables to our database and have slightly changed the database schema to suit our new functionality. We believe we have made a good use of the Django RestAPI which allowed us to enhance our interactions within the database, as well as improve its security. The new database schema can be found in db_schema.pdf. <br />

We had to change our vision for the map due to the difficulties related to ... Currently, our map is displaying the legislators' voting results for each given bill.  <br />

# Anything You'd Like the TA to Know #

This was a challenging milestone. Getting everything to work together was hard, and although we had to lower our expectations for some of the aspects of the app, such as design, we truly believe that the core of the application is present and functions as intended. Working in a big team comes with its own difficulties, and while minor inconsistencies between the expectations and result are bad, they are understandable given it was a first such experience for the most of us. We have learned a lot and now know how challenging the software engineering process can be and which common pitfalls we should avoid.

Should there be any questions regarding the front-end, or accpetance tests please feel free to contact **Yasoob Rasheed**. If anything arises regarding the back-end, please do not hesitate to reach **Larry Chen**.
