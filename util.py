from django.contrib.auth.models import User
from authentication.models import *
from core.models import *
from django.conf import settings
from pyfb import Pyfb

oauth = Pyfb(settings.FACEBOOK_APP_ID, settings.FACEBOOK_SECRET_KEY)
u = User.objects.get(username='igokulnath')
f = FacebookProfiles.objects.get(user=u)
oauth.set_access_token(f.fbk_token)

api = tweepy.API(oauth)
me = api.me()
