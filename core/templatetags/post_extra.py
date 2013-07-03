from django import template
from django.template import Library, Node
from core.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

register = template.Library()
@register.filter
def in_filter(post):
     post = Posts.objects.get(id = post.id)
     comment = post.commenttopost.all()
     return comment

def load_opinion(context,user,post):
    postid=post.id
    print postid
    post = Posts.objects.get(id = post.id )
    l_class = "btn-success"
    dl_class = "btn-success"
    user_opinion = False
    user_opi_val = 0
    opis_count = 0
    dislikes_count = 0
    likes_count = 0

    try:
        opis = post.opinion_to_post.all()
        opis_count = opis.count()
        likes = post.opinion_to_post.filter(opinion = 1)
        likes_count = likes.count()

        dislikes = post.opinion_to_post.filter(opinion = -1)
        dislikes_count = dislikes.count()

        for o in opis:
            if user == o.user:
                user_opinion = True
                user_opi_val = o.opinion

                if user_opi_val == 1:
                    l_class = "btn-danger"
                else:
                    dl_class = "btn-danger"
    except ObjectDoesNotExist:
        print "hee in obje"
        l_class="btn-success"
        dl_class="btn-success"

    return{
        'l_class':l_class,
        'dl_class':dl_class,
        'postid':postid,
        'user_opinion':user_opinion,
        'user_opi_val':user_opi_val,
        'opis_count':opis_count,
        'likes_count':likes_count,
        'dislikes_count':dislikes_count,
        
    }
register.inclusion_tag('includes/opinion.html', takes_context=True)(load_opinion)    
    