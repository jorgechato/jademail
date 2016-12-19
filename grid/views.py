from django.views.generic import ListView
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required

from .models import List
from .models import Person
from .models import Template


# @login_required()
class ListListView(ListView):
    queryset = List.objects.all()
    context_object_name = 'lists'


class PersonListView(ListView):
    queryset = Person.objects.all()
    context_object_name = 'people'


class PersonDetailView(DetailView):
    model = Person


class TemplateListView(ListView):
    queryset = Template.objects.all()
    context_object_name = 'templates'


class TemplateDetailView(DetailView):
    model = Template
