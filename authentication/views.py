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