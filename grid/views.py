from django.views.generic import ListView
from django.views.generic import DetailView
from braces import views

from .models import List
from .models import Person
from .models import Template


class ListListView(
        views.LoginRequiredMixin,
        ListView):
    queryset = List.objects.all()
    context_object_name = 'lists'


class PersonListView(
        views.LoginRequiredMixin,
        ListView):
    queryset = Person.objects.all()
    context_object_name = 'people'


class PersonDetailView(
        views.LoginRequiredMixin,
        DetailView):
    model = Person


class TemplateListView(
        views.LoginRequiredMixin,
        ListView):
    queryset = Template.objects.all()
    context_object_name = 'templates'


class TemplateDetailView(
        views.LoginRequiredMixin,
        DetailView):
    model = Template
