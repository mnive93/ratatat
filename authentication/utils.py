import tweepy
from django.conf import settings

def get_api(request):
        # set up and return a twitter api object
        oauth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
        access_key = request.session['access_key_tw']
        access_secret = request.session['access_secret_tw']
        oauth.set_access_token(access_key, access_secret)
        api = tweepy.API(oauth)
        return api