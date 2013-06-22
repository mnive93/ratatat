import datetime
from haystack import indexes
from code.models import Posts


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    content = indexes.CharField(document=True, use_template=True)
    user = indexes.CharField(model_attr='user')
    time_created = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return Note

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(time_created__lte=datetime.datetime.now())