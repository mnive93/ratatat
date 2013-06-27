from django.db import models
from django.contrib.auth.models import User

class Genres(models.Model):
	title = models.CharField(max_length=64)
	identifier = models.CharField(max_length=32)
	users = models.ManyToManyField(User, related_name='genretouser')

class Posts(models.Model):
	user = models.ForeignKey(User)
	genres = models.ManyToManyField(Genres, related_name="posttogenre")
	time_created = models.DateTimeField(auto_now_add = True)
	time_updated = models.DateTimeField(auto_now_add = True)
	popularity = models.IntegerField(default=1)
	content = models.CharField(max_length = 255)
	source = models.CharField(max_length=3)
class Comments(models.Model):
    comment = models.CharField(max_length=250)
    user = models.ForeignKey(User)
    post = models.ManyToManyField(Posts,related_name="commenttopost")
    time_log = models.DateTimeField(auto_now_add=True)
class OpinionManager(models.Manager):
    def likers(self, post):
        try:
            likes = self.filter(post = post, opinion = 1).all()
            likers = []
            for l in likes:
                likers.append(l.user)
        except ObjectDoesNotExist:
            pass

        return likers

    def dislikers(self, post):
        try:
            dislikes = self.filter(post = post, opinion = -1).all()
            dislikers = []
            for d in dislikes:
                dislikers.append(d.user)
        except ObjectDoesNotExist:
            pass

        return dislikers

class Opinions(models.Model):
    user = models.ForeignKey(User, related_name = 'opinion_to_user')
    post = models.ForeignKey(Posts, related_name = 'opinion_to_post')
    opinion = models.IntegerField(default = 0)
    time_log = models.DateTimeField(auto_now_add = True)
    objects = OpinionManager()
