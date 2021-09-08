from django.conf.urls import url
from .views import BookListView, BookDetailView


urlpatterns = [
    url(r'^$', BookListView.as_view()),
    url(r'^(?P<pk>\d+)$', BookDetailView.as_view()),
]
