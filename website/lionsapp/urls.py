from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'lionsapp'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^checkin/(?P<id>\d+)$', view=views.checkin, name ='checkin'),
    url(r'^new$',views.HabbitCreate.as_view(),name='habbit_new',),
]
