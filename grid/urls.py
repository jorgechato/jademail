from django.conf.urls import url

from views import PersonDetailView
from views import PersonListView
from views import ListListView
from views import TemplateListView
from views import TemplateDetailView

app_name = 'grid'

urlpatterns = [
        url(r'^$', ListListView.as_view(), name='list'),
        url(r'^(?P<Lists_id>[-\w]+)/$', PersonListView.as_view(), name='list_detail'),
        url(r'^(?P<lists_id>[-\w]+)/(?P<slug>[-\w]+)/$', PersonDetailView.as_view(), name='people_detail'),
        url(r'^templates/(?P<slug>[-\w]+)/$', TemplateDetailView.as_view(), name='template_list'),
        url(r'^templates/$', TemplateListView.as_view(), name='template_detail'),
        ]
