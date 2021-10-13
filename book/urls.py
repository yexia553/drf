from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()

router.register('bookinfos', views.BookInfoModelViewSet, basename='bookinfo')
router.register('heroinfos', views.HeroInfoModelViewSet, basename='heroinfo')

urlpatterns = [
    # url(r'^$', views.BookListView.as_view()),
    # url(r'^(?P<pk>\d+)$', views.BookDetailView.as_view()),
    # url(r'^bookinfos/$', views.BookInfoViewSet.as_view({'get':'list', 'post':'create'})),
    # url(r'^bookinfos/(?P<pk>\d+)$', views.BookInfoViewSet.as_view({'get':'retrieve', 'put':'update', 'delete':'delete'})),
    # url(r'^bookinfos/latest/$', views.BookInfoViewSet.as_view({'get':'latest'})),

] + router.urls
