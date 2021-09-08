from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()

router.register('', views.BookInfoView, basename='books')

urlpatterns = [
    # url(r'^$', views.BookListView.as_view()),
    # url(r'^(?P<pk>\d+)$', views.BookDetailView.as_view()),
] + router.urls
