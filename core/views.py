from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.conf import settings
from django.template import RequestContext, Context
from authentication.models import *
from core.models import *
from authentication.forms import *
from core.forms import *
from pyfb import Pyfb
import datetime, random, tweepy, shlex


def feed(request):
	usergenres = request.user.genretouser.all()
	user = request.user
	if request.method == 'POST':
		form = PostingForm(request.POST)

		if form.is_valid():
			post = Posts.objects.create(
				user=user,
				content = form.cleaned_data['content'],
				time_created=datetime.datetime.now(),
				time_updated=datetime.datetime.now(),
				source='lw',
				popularity=1
			)

			if request.POST.get('facebookshare'):
				try:
					fb = FacebookProfiles.objects.get(user=user)
					fbk = Pyfb(settings.FACEBOOK_APP_ID, settings.FACEBOOK_SECRET_KEY)
					fbk.set_access_token(fb.fbk_token)

					fbk.publish(message=form.cleaned_data['content'], id=fb.fbk_id)
				except ObjectDoesNotExist:
					pass

			if request.POST.get('twittershare'):
				try:
					tw = TwitterProfiles.objects.get(user=user)
					twttr = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
					twttr.set_access_token(tw.oauth_token, tw.oauth_secret)
					api = tweepy.API(twttr)
					me = api.me()
					api.update_status(form.cleaned_data['content'] + ' via @likewyss')
				except ObjectDoesNotExist:
					pass

			return HttpResponseRedirect('/feed/')
	else:
		form = PostingForm()

	var = RequestContext(request, {
		'form':form,
        'user':request.user,
        'genres':usergenres
        })
	return render_to_response('pages/feed.html', var)

def profile(request, username):
	user = get_object_or_404(User, username=username)
	sta = rtwts = fb = tw = None
	try:
		fbk = FacebookProfiles.objects.get(user=user)
	except ObjectDoesNotExist:
		pass

	try:
		twttr = TwitterProfiles.objects.get(user=user)
	except ObjectDoesNotExist:
		pass

	posts = Posts.objects.filter(user=user).order_by('-time_created')

	var = RequestContext(request, {
		'user':user,
		'fb':fbk,
		'tw':twttr,
		'posts':posts
		})

	return render_to_response('pages/profile.html', var)

def search(request):
	if 'q' in request.GET:

		q = request.GET['q']

		usernames = User.objects.filter(username__icontains=q)

		return HttpResponse(usernames)
	else:
		return HttpResponse('Null')