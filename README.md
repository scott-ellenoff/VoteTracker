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

brew install node
npm install
react-native run-ios

This will take a bit of time so hang on. Also, if you get a CFBundleIdentifier error, please contact me at 
yasoobr@uchicago.edu, as this is a compatibility problem with XCode and React Native. 

5. You’re all set! The react-native front-end framework is ready to be viewed.

# How to Compile Back-End #

# How to Run Unit Cases (Acceptance Test Examples) #

# What Has Been Implemented #

On the front-end, we have built a react-native application with stateless design that will segue from view to view and is 
compatible with iOS and Android. We have laid out the framework for our three view design (Home, Main, and Profile Pages). 
The Home Page will be linked with Django/Firebath Auth or Facebook Auth by the next iteration. The Main Page will have a 
view that updates asynchronously with calls to our fully functional Django REST API. The Profile Page will similarly update 
asynchronously. The INFO, and + buttons will take you to an auxiliary screen where you can learn more about a bill or your 
legislators.

# Who Did What? #

Front-End:

Yasoob Rasheed - Worked on React Framework (Home, Main, Segues) <br />
Zach Kamran - Worked on React Framework (Profile, Segues) <br />
Scott Wang - Worked on mock-up of design, really helping us structure the design of our components well <br />

# Have We Made Any Changes? #

# Anything You'd Like the TA to Know #

We wanted to implement more of the front-end but believe that there is no use for overly flowery design without all pieces 
coming together and functioning first. We have built a really solid framework and are excited to go from there once the 
database is fully operational.
