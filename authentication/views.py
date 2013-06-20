from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import login,logout
from django.template import RequestContext, Context
from django.template.loader import get_template
from django.core.mail import send_mail
from django.conf import settings
from authentication.models import *
from core.models import *
from authentication.forms import *
from pyfb import Pyfb
import datetime, random, tweepy, shlex

'''
The following view function, lr, is to redirect an unauthenticated user to the home page if he tries to access a page, say Settings or Feed, that requires authentication. The one that follows that, nlr does the opposite of the lr function. If a logged in user tries to access a page that can be accessed only when logged out, such as the signup page or the landing page, he will be redirected to the feed page URL.

'''

def randomnumber():
	randomnum = random.randint(0,1000000)
	return randomnum

def signupmail(emailaddress, identifier):
	template = get_template('emails/signup.txt')
	context = Context({
		'email':emailaddress,
		'link':settings.SITE_HOST + 'signup/' + str(identifier)
		})
	message = template.render(context)
	from_email = settings.ADMINS[0][0]
	to_email = emailaddress
	subject = "Thank you for signing up at Likewyss."

	send_mail(subject = subject, from_email = from_email, message = message, recipient_list = [emailaddress])

def lr(view):
    def new_view(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/')
        return view(request, *args, **kwargs)
    return new_view

def nlr(view):
    def new_view(request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/feed/')
        return view(request, *args, **kwargs)
    return new_view

def hello(request):
    if request.method=='POST':
        form = EmailForm(request.POST)

        if form.is_valid():
        	email = form.cleaned_data['email']
        	signuppending = existingaccount = None

        	try:
        		existingaccount = User.objects.get(email = email)
        	except ObjectDoesNotExist:
        		try:
	        		signuppending = SignupHandler.objects.get(emailaddress = email)
	        	except ObjectDoesNotExist:
        			handlesignup = SignupHandler.objects.create(
        				emailaddress = email,
        				identifiernum = randomnumber()
        			)

        			signupmail(handlesignup.emailaddress, handlesignup.identifiernum)
        	
        	if signuppending:
        		return render_to_response('registration/signup/pending.html', {'email':signuppending.emailaddress})
        	elif existingaccount:
        		return render_to_response('registration/signup/existing.html', {'email':existingaccount.email})
        	else:
        		return render_to_response('registration/signup/success.html', {'email':handlesignup.emailaddress})
    else:
    	form = EmailForm()

    var = RequestContext(request, {
        'form':form
    })
    
    return render_to_response('pages/landing.html', var)

'''

The following view functions login and logout do their jobs as the names depict, respectively.

'''

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')

'''

When the user clicks the signup link, he will be redirected to this page which matches the number in the URL to an object in the SignupHandler model.

'''

def signup(request, number):
    signup = get_object_or_404(SignupHandler, identifiernum=number)

    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            name_split = shlex.split(form.cleaned_data['fullname'])
            fname = name_split[0]
            lname = ''
            for x in name_split[1:]:
                lname += (x + ' ')
            user = User.objects.create_user(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password'],
                email = signup.emailaddress,
                first_name = fname,
                last_name = lname
            )
            login(request, user)
            return HttpResponseRedirect('/auth/welcome/')
    else:
        form = SignupForm()

    var = RequestContext(request, {
        'form':form,
        'email':signup.emailaddress
        })

    return render_to_response('registration/signup/signup.html', var)

'''

Social account integration is a huge pain in Django. Unlike Ruby which has extremely amazing gems such as omniauth, Python-Django does not have such luxuries. We are using Pyfb for Facebook and Tweepy for Twitter integrations. Every social authentication system comprises of three parts -- one that calls the API and redirects you to the permission page, the other one that gets back the token and takes you to the callback URL, and the last one, called the Prestige :D , that adds the tokens and keys to the database.

'''

def beginFbAuth(request):
    facebook = Pyfb(settings.FACEBOOK_APP_ID)
    return HttpResponseRedirect(facebook.get_auth_code_url(redirect_uri=settings.FACEBOOK_SIGNUP_REDIRECT_URL))

def facebooksignupsuccess(request):
    code = request.GET.get('code')    
    facebook = Pyfb(settings.FACEBOOK_APP_ID)
    fb_token = facebook.get_access_token(settings.FACEBOOK_SECRET_KEY, code, redirect_uri=settings.FACEBOOK_SIGNUP_REDIRECT_URL)
    me = facebook.get_myself()

    try:
        user = User.objects.get(email = me.email)
        try:
            fbk = FacebookProfiles.objects.get(user = user)
        except ObjectDoesNotExist:
            fbk = FacebookProfiles.objects.create(
                user = user,
                fbk_id = me.id,
                fbk_token = fb_token
            )
        login(request, user)
        return HttpResponseRedirect('/feed/')
    except ObjectDoesNotExist:
        user = User.objects.create_user(
            username = me.username,
            email = me.email
            )

        fbk = FacebookProfiles.objects.create(
            user = user,
            fbk_id = me.id,
            fbk_token = fb_token
        )

        name_split = shlex.split(me.name)
        fname = name_split[0]
        lname = ''
    
        for x in name_split[1:]:
            lname += (x + ' ')

        user.first_name = fname
        user.last_name = lname
            
        user.save()

        return HttpResponseRedirect('/setpwd/%s' % str(me.id))

def setpassword(request, idnum):

    idnum = int(idnum)

    try:
        fb = FacebookProfiles.objects.get(fbk_id = idnum)
        facebook = Pyfb(settings.FACEBOOK_APP_ID)
        facebook.set_access_token(fb.fbk_token)
        me = facebook.get_user_by_id(id = fb.fbk_id)
        user = fb.user
    except ObjectDoesNotExist:
        return HttpResponseRedirect('/landing/')

    if request.method == 'POST':
        form = PasswordSetForm(request.POST)

        if form.is_valid():
            user.set_password(form.cleaned_data['password'])
            user.save()
            return HttpResponseRedirect('/login/')
    else:
        form = PasswordSetForm()

    var = RequestContext(request, {
        'form':form,
        'me':me,
        'user':user
        })

    return render_to_response('registration/facebook.html', var)

'''

Twitter signup is a little bit more complicated than Facebook because Twitter does not give us the user's email address.
We, however, need it. Therefore, in the final step, we will be collecting the user's email address in addition to the password as is being set in the facebook signup process.

'''

def beginTwitterAuth(request):
    # start the OAuth process, set up a handler with our details
    oauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    
    # direct the user to the authentication url
    # if user is logged-in and authorized then transparently goto the callback URL
    
    auth_url = oauth.get_authorization_url(True)
    response = HttpResponseRedirect(auth_url)
    
    # store the request token
    request.session['unauthed_token_tw'] = (oauth.request_token.key, oauth.request_token.secret)
    request.session.save()
    request.session.modified=True
 
    return response 

def twitterCallback(request):
    verifier = request.GET.get('oauth_verifier')
    oauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    token = request.session.get('unauthed_token_tw', None)
    # remove the request token now we don't need it
    request.session.delete('unauthed_token_tw')
    request.session.modified=True
    oauth.set_request_token(token[0], token[1])
    # get the access token and store
    try:
        oauth.get_access_token(verifier)
    except tweepy.TweepError:
        print 'Error, failed to get access token'
    request.session['access_key_tw'] = oauth.access_token.key
    request.session['access_secret_tw'] = oauth.access_token.secret    
    response = HttpResponseRedirect('/addtwitter/')
    return response
 
def info(request):
    api = get_api(request)
    me = api.me()
    user = User.objects.create_user(
            username = me.screen_name,
        )

    name_split = shlex.split(me.name)
    fname = name_split[0]
    lname = ''
    
    for x in name_split[1:]:
        lname += (x + ' ')

    user.first_name = fname
    user.last_name = lname
            
    user.save()

    twttr = TwitterProfiles.objects.create(
            user = user,
            oauth_token = request.session['access_key_tw'],
            oauth_secret = request.session['access_secret_tw']
        )

    return HttpResponseRedirect('/setpwd/twitter/%s' % str(user.id))

def setpwdtwttr(request, idnum):
    try:
        user = User.objects.get(id = int(idnum))
        tw_user = TwitterProfiles.objects.get(user = user)
    except ObjectDoesNotExist:
        raise Http404

    api = get_api(request)
    me = api.me()

    if request.method == 'POST':
        form = TwitterSignupForm(request.POST)

        if form.is_valid():
            try:
                twuser = User.objects.get(email = form.cleaned_data['email'])
                twuser.username = me.screen_name
                twuser.save()
                tw_user.user = twuser
                tw_user.save()
            except ObjectDoesNotExist:
                user.email = form.cleaned_data['email']
                user.set_password(form.cleaned_data['password'])
                user.save()
            return HttpResponseRedirect('/login/')
    else:
        form = TwitterSignupForm()

    var = RequestContext(request, {
        'form':form,
        'me':me
        })

    return render_to_response('registration/tw.html', var)

def check_key(request):
    """
   Check to see if we already have an access_key stored, if we do then we have already gone through
   OAuth. If not then we haven't and we probably need to.
   """
    try:
        access_key = request.session.get('access_key_tw', None)
        if not access_key:
            return False
    except KeyError:
        return False
    return True

def welcome(request):
    genres = Genres.objects.all()
    u = request.user
    if request.method == 'POST':
        genrelist = request.POST.getlist('selectedgenres')
        
        for itemid in genrelist:
            g = Genres.objects.get(id=itemid)
            u.genretouser.add(g)

        return HttpResponseRedirect('/feed/')

    else:
        var = RequestContext(request, {
            'user':request.user,
            'genres':genres
            })
        return render_to_response('registration/signup/genres.html', var)