from django import template
from core.models import *
register = template.Library()
@register.filter
def in_filter(post):
     post = Posts.objects.get(id = post.id)
     comment = post.commenttopost.all()
     return comment
