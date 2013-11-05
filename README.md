## Instagram API Flask example

Using the wonderful [Python-Instagram library](https://github.com/Instagram/python-instagram)

### Requirements

* Python 2.7.x
* Virtualenv
* PIP
* Heroku Toolbelt / Foreman
* Instagram Account

How to install these requirements is [here](http://itppyweb.herokuapp.com/notes/week_1), halfway down page

## How to run locally

### Download code

## Set up virtual environment

Navigate to code directory in Terminal and run following command

* Create and activate virtual environment for directory.

		virtualenv venv
		. venv/bin/activate

* Install requirements for app

		pip install -r requirements.txt


## Create Instagram Application/Account

* Create new app here, <http://instagram.com/developer/clients/register/>.
* Set OAuth redirect_uri to 

		http://localhost:5000/instagram_callback


### Set up Instagram Credentials

In your Application settings, find the tokens and keys, you will need these to use the Instagram API.

Create **.env** file with the following


	CLIENT_ID=YOURCLIENTIDHERE
	CLIENT_SECRET=YOURCLIENTSECRETHERE
	SECRET_KEY=SECRET_KEY_FOR_FLASK
	REDIRECT_URI=http://localhost:5000/instagram_callback

Save as **.env** in your code directory.


## Start the server

To start server you must have Foreman / [Heroku toolbelt](http://toolbelt.heroku.com) installed. Foreman will read your .env files to get your credentials.

Start your engines

	foreman start

OR

	. start

### Enjoy

Open browser, <http://localhost:5000>


### Stop server 

	Ctrl+C

