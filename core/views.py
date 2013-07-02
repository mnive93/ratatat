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
import redis
import json
from django.views.decorators.csrf import csrf_exempt

def feed(request):
	usergenres = request.user.genretouser.all()
	user = request.user
	if request.method == 'POST':
		form = PostingForm(request.POST)

		if form.is_valid():

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
	'''
	try:
		fbk = FacebookProfiles.objects.get(user=user)
	except ObjectDoesNotExist:
		pass

	try:
		twttr = TwitterProfiles.objects.get(user=user)
	except ObjectDoesNotExist:
		pass
   '''
	posts = Posts.objects.filter(user=user).order_by('-time_created')
	comments = Comments.objects.all()
	var = RequestContext(request, {
		'user':user,
	#	'fb':fbk,
	#	'tw':twttr,
		'posts':posts,
		})

	return render_to_response('pages/profile.html', var)
def search(request):
	if 'q' in request.GET:

		q = request.GET['q']

		usernames = User.objects.filter(username__icontains=q)

		return HttpResponse(usernames)
	else:
		return HttpResponse('Null')

 
@csrf_exempt
def postdata(request):  
   if request.method == "POST":
    print "in my view"
    sender = User.objects.get(id=request.POST.get("sender"))  
    print request.POST.get("sender")
    random
    text = request.POST['message']
    decision = 'undefined'
    post = Posts.objects.create(
				user=sender,
				content = text,
				time_created=datetime.datetime.now(),
				time_updated=datetime.datetime.now(),
				source='lw',
				popularity=1
			)
    
    r = redis.StrictRedis()
    r.publish('feed', json.dumps({
            "sender": sender.username,
            "text": text,
        }))
    return HttpResponse(json.dumps({"status": "ok"}), content_type="application/json")
@csrf_exempt
def commentdata(request):  
   if request.method == "POST":
    sender = User.objects.get(id=request.POST.get("sender"))  
    text = request.POST['message']
   

    post = Posts.objects.get(id=request.POST.get("post_id"))
    print post
    print text
    comment = Comments.objects.create(
    	            comment=text,
    	            user=sender,
    	            time_log=datetime.datetime.now(),

    	)
    comment.post.add(post)
    r = redis.StrictRedis()
    r.publish('comment', json.dumps({
            "sender": sender.username,
            "text": text,
        }))

    return HttpResponse(json.dumps({"status": "ok"}), content_type="application/json")

@csrf_exempt
def opinion(request):
    if request.method == 'POST':
        post_id = request.POST['post_id']
        value = request.POST['value']
        post = Posts.objects.get(id = post_id)
        user = User.objects.get(id=request.POST.get("sender"))  
        try:
            u_opinion = Opinions.objects.get(
                user = user,
                post = post
            )
            if value == '0':
                u_opinion.delete()
            else:
                u_opinion.opinion = value 
                u_opinion.save()
                
        except ObjectDoesNotExist:
            u_opinion = Opinions.objects.create(
                    user = user,
                    post = post,
                    opinion = value
            )
    return HttpResponse(json.dumps({"status": "ok"}), content_type="application/json")
