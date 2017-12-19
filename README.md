Web Software Development 2017 Project Plan
-----------------------

### 1. Team

* 528579 Nikolas Erkinheimo
* 479518 Kaarlo Kekkonen
* 530020 Carl Eric Pellja


### 2. Goal

The goal of this project is to make a gamestore. In addition to functionality emphasis will be on good and readable code. Minimum requirements will be met and so will most of the additional ones. A good grade is something we will strive for.


### 3. Plans

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


### 4. Process and Time Schedule

We will begin working on the project Jan 2nd. Meetings will be arranged in 2 week intervals and communication will primarily be done via Telegram. Different features will be assigned off the record to team members and will be developed in branches. After feature is functional and all possible related tests are passed the feature will be merged with master. 


### 5. Risk Analysis

Perceived problems will be addressed as soon as possible. If development is slow additional meetings will be arranged.
