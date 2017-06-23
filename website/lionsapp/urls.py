from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'lionsapp'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^trait/good/new$',views.GoodTraitCreate.as_view(), name='new_good_trait',),
    url(r'^trait/good/checkin/(?P<id>\d+)$', view=views.checkin, name ='checkin'),
    url(r'^trait/good/undocheckin/(?P<id>\d+)$', view=views.undo_checkin, name ='undo_checkin'),
    url(r'^trait/good/delete/(?P<id>\d+)$', view=views.delete_good_trait, name ='undo_checkin'),

    url(r'^trait/bad/new$',views.BadTraitCreate.as_view(), name='new_good_trait',),
    url(r'^trait/bad/actout/(?P<id>\d+)$', view=views.actout, name ='checkin'),
    url(r'^trait/bad/undoactout/(?P<id>\d+)$', view=views.undo_actout, name ='undo_checkin'),
    url(r'^trait/bad/delete/(?P<id>\d+)$', view=views.delete_bad_trait, name ='undo_checkin'),
]
