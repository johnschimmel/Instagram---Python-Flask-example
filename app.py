import os
import time
from instagram.client import InstagramAPI
from flask import Flask, request, render_template, session, redirect, abort, flash, jsonify

app = Flask(__name__)   # create our flask app
app.secret_key = os.environ.get('SECRET_KEY')


# configure Twitter API
instaConfig = {
	'client_id':os.environ.get('CLIENT_ID'),
	'client_secret':os.environ.get('CLIENT_SECRET'),
	'redirect_uri' : os.environ.get('REDIRECT_URI')
}
api = InstagramAPI(**instaConfig)

@app.route('/')
def user_photos():


	if 'instagram_access_token' in session and 'instagram_user' in session:
		userAPI = InstagramAPI(access_token=session['instagram_access_token'])
		recent_media, next = userAPI.user_recent_media(user_id=session['instagram_user'].get('id'),count=25)

		templateData = {
			'size' : request.args.get('size','thumb'),
			'media' : recent_media
		}

		return render_template('display.html', **templateData)
		

	else:
		return redirect('/connect')


@app.route('/json')
def json():
	
	if 'instagram_access_token' in session and 'instagram_user' in session:
		userAPI = InstagramAPI(access_token=session['instagram_access_token'])
		recent_media, next = userAPI.user_recent_media(user_id=session['instagram_user'].get('id'),count=25)

		photos = []
		for media in recent_media:
			# photos.append(media.get_standard_resolution_url())  # big photo
			photos.append(media.images['thumbnail'].url) #thumbnails


		return jsonify({
			'status' : 'OK',
			'media' : photos,
			
		})

	else:
		return redirect('/connect')

@app.route('/connect')
def main():

	url = api.get_authorize_url(scope=["likes","comments"])
	return redirect(url)

@app.route('/instagram_callback')
def instagram_callback():

	code = request.args.get('code')

	if code:

		access_token, user = api.exchange_code_for_access_token(code)
		if not access_token:
			return 'Could not get access token'

		app.logger.debug('got an access token')
		app.logger.debug(access_token)
		session['instagram_access_token'] = access_token
		session['instagram_user'] = user

		return redirect('/') # redirect back to main page
		
	else:
		return "Uhoh no code provided"





@app.route('/search')
def itp_tweets():

	# get search term from querystring 'q'
	query = request.args.get('q','#redburns')

	# search with query term and return 10
	results = twitter.search.tweets(q=query, count=50)
	
	templateData = {
		'query' : query,
		'tweets' : results.get('statuses')
	}

	return render_template('search.html', **templateData)



	
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


# This is a jinja custom filter
@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    pyDate = time.strptime(date,'%a %b %d %H:%M:%S +0000 %Y') # convert twitter date string into python date/time
    return time.strftime('%Y-%m-%d %h:%M:%S', pyDate) # return the formatted date.
    
# --------- Server On ----------
# start the webserver
if __name__ == "__main__":
	app.debug = True
	
	port = int(os.environ.get('PORT', 5000)) # locally PORT 5000, Heroku will assign its own port
	app.run(host='0.0.0.0', port=port)