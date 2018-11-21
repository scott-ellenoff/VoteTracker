# Milestone 4a #

1. What we are implementing for this iteration: 
 
For the second iteration, we plan to connect the backend to the front-end and add new features. More specifically, we want to execute on the Django REST API and AWS server we’ve built and actually integrate response/requests into our front-end code. We are going to finish the user login portion, develop push notifications, update the bill and voting information, develop a matching algorithm, and finally develop the map. This seems like a lot, but we’ve split up the tasks well.
 
2. How the work is divided:
 
Map: visualizing how the United States has voted on a specific bill
* Hasmik 
 
Connect front and backend: passing data back and forth from the client and server
Scott E
* Yasoob: generalizing this data in component state, to pass it from View Controller to View Controller in the front-end application
 
Matching algorithm: developing an algorithm to match users with Legislators
* Scott E.
 
Push notifications: sending a push notification every time that a bill is voted on
* Emily: setting up push notifications with Firebase Cloud Messaging and Apple Push Notification System to work with Django
* Yasoob: syncing data with React-Native ios push notifications
 
Updating bill/votes: updating bill and voting information on the client side from the server
* Stepan
* Zach
* Yasoob: sending bill information to the Main page so that Users can vote and see their history
 
Finish user login: authenticating users and fetching their data for client side loading
* Larry: Setting up a registration form, login/logout endpoint, and adding permissions to certain endpoints so that only authenticated users can access their user information.
* Scott W.
 
Deploying the server: deploying the AWS Server for use by the front-end
* Larry: Launching an Amazon EC2 instance and deploying the django backend server in production mode.
 
3. Tests

Our tests are located in VoteTracker/backend/votetrackr_api/tests.py.

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
* Push notifications
* Updating the bill/votes database
* User login

We have chosen to write tests for the above using python's unittest library. With regards to server deployment, that will happen as we are doing iteration 4b. Testing connection of frontend and backend also will be done through our existing tests that call the Django API.


# How To Compile Front-End #

Requirements:

XCode 10.1
Homebrew v1.8.1
Node v8.11.3
NPM v6.4.1

1. Clone the git repository for front-end at:

https://github.com/scott-ellenoff/VoteTracker/tree/front-end

2. Install homebrew
3. Navigate to the folder at which you’ve downloaded the front-end project
4. Run the following commands:


```python
brew install node
npm install 
react-native run-ios
```
This will take a bit of time, so hang on. Also, if you get a CFBundleIdentifier error, please contact me at yasoobr@uchicago.edu, as this is a compatibility problem with XCode and React Native. 

5. You’re all set! The react-native front-end framework is ready to be viewed.

# How to Run Back-End #

Before running the python/django server, make sure python 3.7 is installed. To install the necessary packages, run

```
pip install -r requirements.txt
```

To run the server locally run
```
python manage.py runserver
```

Then, navigate to http://localhost:8000 to access the root endpoint. From there, click on the urls to see the users, bills, legislators, and votes in our database. You use the django-rest-framework ui to make http requests (GET, POST, PUT, DELETE) that will query or make changes to the database.

# How to Run Unit Cases (Acceptance Test Examples) #

To run the unit tests for the backend api run:
```
cd src/backend
python manage.py test
```
This will create a test database and run our unit tests.

# What Has Been Implemented #
**Front-End:** <br />
On the front-end, we have built a react-native application with a stateless design that will segue from view to view and is compatible with iOS and Android. We have laid out the framework for our three view design (Home, Main, and Profile Pages). <br />
The Home Page will be linked with Django/Firebath Auth or Facebook Auth by the next iteration. The Main Page will have a view that updates asynchronously with calls to our fully functional Django REST API. The Profile Page will similarly update asynchronously. The INFO, and + buttons will take you to an auxiliary screen where you can learn more about a bill or your legislators. <br />

**Back-End:** <br />
On the back-end we started with creating scripts to scrape raw data for the legislator voting records, information on bills, and the legislator personal information. That data was later cleaned to suit our needs, more specifically, we only chose the required personal legislator information, cleaned out bill records so the ones that are stored in our database, are relevant to the end-users (sorted by pressing issues). We are planning to use those bills with already existing voting records for calibrating the political preferences of our users and matching them with the legislators. <br />
We have successfully set up a MySQL database, hosted on AWS, and populated it with the scraped and cleaned data on legislators and bills. <br />
We have also developed two rounds of unit tests. The first one, developed for the Milestone 3a, was not comprehensive due to the fact that we were not completely decided on which back-end framework we should use. Hence the tests lacked the details and existed more for the documentation purposes, serving as a goal to what functionality should be implemented and tested by the end of the first iteration. The second round of tests was done in Django to test the functionality of submitting get, post, put, and delete commands to the server. Current test suite tests the same functionality as the tests submitted for the previous Milestone, but it utilises Django API rather than the direct functionality testing. We have also made some changes following the feedback to our Milestone 3a submission, adding tests for addVote() and removeUser() functions, making sure the User cannot vote on the same bill twice and that the removed user disappears from our database. We have also fixed the compilability of our tests. <br />
For the Django API, we created the endpoints and the models that the front-end will be interacting with. This involves connecting the API with the database and recreating the schematics used in the database in Django. The models include the functionality and the endpoints of the API. <br />



# Who Did What? #

**Front-End:** <br />

Yasoob Rasheed - Worked on React Framework (Home, Main, Segues) <br />
Zach Kamran - Worked on React Framework (Profile, Segues) <br />
Scott Wang - Worked on mock-up of design, really helping us structure the design of our components well <br />

**Back-End:** <br />
Larry Chen, Emily Xue, Scott Ellenoff - Worked together to create the Django API <br />
Scott Ellenoff, Stepan Severov - Wrote the original unit tests <br />
Scott Ellenoff, Larry Chen - Updated the backend unit tests to be compatible with the Django API <br />
Hasmik Grigoryan, Stepan Severov - Design and creation of the MySQL AWS database <br />
Stepan Severov - Data scraping and cleaning. Populating the database with the cleaned data <br />

# Have We Made Any Changes? #

We have made some design changes from our proposal. The main one is that now there is a table of Votes which stores voting records for both Users and Legislators, recording their ID, the Bill ID that was voted, and the vote result. Due to that design change, we do not need to store the dictionary of votes in the Person class - we can get the voting records for them by querying the database with their ID. <br />

PullLegislatorVotes() functionality that was planned to be implemented inside the Bill class, now will be running as a cron process on the server side due to that being easier, considering we are using an external ProPublica API to pull records on any new votes which were made public. After obtaining those votes, we update the Votes table described above, recording the legislators’ voting decisions. <br />

Unfortunately, we needed to adjust our functionality requirements for this iteration as learning how to operate the Django framework, setting up the database and writing comprehensive tests took longer than expected. That being said, we are adding the automatic vote-updating cron process and matching algorithm into the next iteration of development. <br />

# Anything You'd Like the TA to Know #

To better understand our design please make sure to see our Database schema (db_schema.pdf) <br />

We wanted to implement more of the front-end but believe that there is no use for overly flowery design without all pieces coming together and functioning first, so instead we have built a really solid framework and are excited to go from there once the database is fully operational.
As per the backend, we now have a strong base, upon which we will be implementing the additional functionality. <br />
For most of us it is our first experience working closely in such a big group, but we believe it is going great!
