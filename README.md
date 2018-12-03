# Milestone 4b #

# Installation Guide #

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

