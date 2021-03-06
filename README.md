Web Software Development 2017 Project Plan
-----------------------


### 1. Team

* 528579 Nikolas Erkinheimo
* 479518 Kaarlo Kekkonen
* 530020 Carl Eric Pellja

# 1. Project Plan #

### 1.2 Goal

The goal of this project is to make a gamestore. In addition to functionality emphasis will be on good and readable code. Minimum requirements will be met and so will most of the additional ones. A good grade is something we will strive for.


### 1.3 Plans ###

There will be two kinds of users in this store: players and developers. Developers also possess the same abilities as the players (they will be able to purcahse games, even their own one if they so desire). Developers will be able to add games to the store and analyze sale statistics. Players will be able to buy and play games and interact with high scores.

The URL schema will be close to the following (in addition to /):

/game/<slug>
/search
/categories
/account
/login
/register
/verify
/notfound

In one way or another there will be at least following models:

Player, Developer
Purchase
Game
GameSave

Authentication will be implemented by using Django's own user model and extending it with necessary information. Email validation will be in the /verify path: user will get the verification email and by clicking a link in it the account associated with the link will be verified in the database. The site will have a category listing and search functionality. Niksula payment api will be used for transactions. Players will only be able to play games that they have paid for and developers can modify game information only on games related to their account. Games and the store will make contact via window.postMessage. This will be used in following situtations: saving game state, loading game state and posting high score.

In addition to mandatory requirements many of the listed additional features will be implemented such as save/load, RESTful API, mobile friendly UI and social media sharing. If additional time will be left after all this, 3rd party login will also be attempted.

One of our important personal goals is to make really good code. Refactoring is allowed and encouraged.


### 1.4 Process and Time Schedule

We will begin working on the project Jan 2nd. Meetings will be arranged in 2 week intervals and communication will primarily be done via Telegram. Different features will be assigned off the record to team members and will be developed in branches. After feature is functional and all possible related tests are passed the feature will be merged with master.


### 1.5 Risk Analysis

Perceived problems will be addressed as soon as possible. If development is slow additional meetings will be arranged.

# 2. Documentation #

### 2.1 Description ###
This is a online gamestore made for the Aalto Web Software Developement course using Django framework.

The website's users are divided into players and developers. A player can browse and purchase games, and view his game inventory. A developer has the same (kyvyt) as the player, but he can also add
games, edit/delete them and view sales statistics. The games are paid using the Aalto university [mockup payment service](http://payments.webcourse.niksula.hut.fi/)

The website is deployed on heroku at <http://protected-anchorage-48125.herokuapp.com>

Tools used: HTML5, CSS (+Bootstrap), JS (+Jquery, Chart.js), Django Framework (+Python 3.6)

### 2.2 Project requirements ###

#### Minimum requirements ####

User can register as a player or a developer. Developers can add games to their inventory and manage their games. Players buy/play games, see high scores and save their own scores.

#### Authentication ####

Players and developers can register/login/logout. Email validation is done with django console backend. On heroku a link leading to the activation url is shown after successfull registration. The activation token is made with Django's PasswordResetTokenGenerator

#### Basic player functionalities ####

Players can buy games using the courses mockup payment service. After buying the game the player can play the game.
more about player stuff here

#### Basic developer functionalities ####

Developers can add/modify/delete games they own. Developers can also see sales statistics of their games.

#### Game/service interaction ####

The service supports the course project message protocol. Users can save their high score, if the game supports such feature. More about game/service interaction on 2.4 Save/load feature.

#### Quality of Work ####

html, css and js files have been validated using W3C Validation service and JSlint. The website has also rigorious manual tests.

A large emphasis has been placed to site security. Django requires a csrf token for all POST messages, including those used in game messaging.

Unfortunately our site is not very modular, as we chose to not split each feature in a separate app.

### 2.3 Additional Features ###

#### Save/load and resolution feature ####

Players can save and load gameStates. The gamestate is saved in the database as a textfield. This enables the custom gamestates for each game. The service only keeps one gamestate per user per game stored. Also supports the SETTING message to set the IFrame width and length.

#### 3rd party login ####

Users can log in using Google accounts. The service uses Python Social Auth app. Users with Google accounts can be both players and developers.

#### RESTful API ####

A simple RESTful api was implemented, which supports available games, high scores and sales for game developers.

#### Mobile Friendly ####

The service was designed to be usable with both traditional computers and smartphones. Tests were done with 1080p screen computers and 4inch smartphones. This mobile friendliness was achieved mostly with the use of Bootstrap.

### 2.5 Instructions ###

the site is hosted at http://protected-anchorage-48125.herokuapp.com.
Users should first sign up as either regular user or developer using signup form at. After creating the account, the user must activate the account using the activation link. The activation link is rendered to the user, and it must be used or it will be lost forever. If the service is running locally the link is also printed on the console using django's console emailbackend. If the user has a google account, it can be used to login without creating a separate account. A player can later request developer rights at profile settings. Only pages accessible without authentication are login, signup, home and some rest urls.

After authenticating the user is redirected to homepage where he can see the 3 best selling games. from the navigation bar it is possible no navigate to game categories, owned games or account setting, or search the games. If the user is developer, he can add games as well as edit his/hers existing games at "my games".

Adding and editing games is done using a form. The form requires a name, url, description, price and category. A image can also be added for the game, but this field is optional. The game price is rounded to 2 decimals.

RESTful api has several functions. 'rest/games' lists all games as a json. 'rest/highscores' lists all scores for all games, and 'rest/sales' lists all the sales of the request sender, if he has developer permissions. 'rest/mygames' lists all the games which are owned by the request sender.

### 2.6 Team workload and points ###

#### Kaarlo Kekkonen ####
Minimum functional requirements, Authentication, Basic player functionalities-payment/play , Basic developer functionalities, Game/service interaction, Save/load and resolution feature, 3rd party login, Mobile Friendly, Non-functional requirements-documentation, Quality of Work-testing/quality of code

#### Nikolas Erkinheimo ####
Minimum functional requirements, RESTful API, Quality of Work-User experience, Mobile Friendly, Non-functional requirements-project plan

#### Carl Eric Pellja ####
Basic player functionalities-categories/search, Quality of Work-User experience

#### Points per feature ####
Authentication-200p  
Basic player functionalities-300p  
Basic developer functionalities-200p  
Game/service interaction-200p  
Quality of Work-75p  
Non-functional requirements-200p  
Save/load and resolution feature-100p  
3rd party login-100p  
RESTful API-100p  
Mobile Friendly-50p  

TOTAL:1525p  
