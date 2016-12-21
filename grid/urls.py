from django.conf.urls import url

from . import views

app_name = 'grid'

urlpatterns = [
        # list
        url(r'^$', views.ListListView.as_view(), name='home'),
        url(r'^contacts/(?P<lists_id>[-\w]+)/$', views.PersonListView.as_view(), name='list_detail'),
        url(r'^templates/$', views.TemplateListView.as_view(), name='template_list'),

        # detail
        url(r'^contact/(?P<slug>[-\w]+)/$', views.PersonDetailView.as_view(), name='people_detail'),
        url(r'^template/(?P<slug>[-\w]+)/$', views.TemplateDetailView.as_view(), name='template_detail'),

        # create
        url(r'^add/$', views.ListCreateView.as_view(), name='list_create'),
        url(r'^add/contact/$', views.PersonCreateView.as_view(), name='people_create'),
        url(r'^add/template/$', views.TemplateCreateView.as_view(), name='template_create'),

        # edit
        url(r'^edit/(?P<slug>[-\w]+)/$', views.ListUpdateView.as_view(), name='list_edit'),
        url(r'^edit/contact/(?P<slug>[-\w]+)/$', views.PersonUpdateView.as_view(), name='people_edit'),
        url(r'^edit/template/(?P<slug>[-\w]+)/$', views.TemplateUpdateView.as_view(), name='template_edit'),

        # delete
        url(r'^delete/contact/(?P<pk>[-\w]+)/$', views.PersonRemoveView.as_view(), name='people_delete'),

        # send email
        url(r'^send/(?P<tp_pk>[-\w]+)/(?P<to_pk>[-\w]+)/$', views.SendEmailView.as_view(), name='send_email'),
        ]
