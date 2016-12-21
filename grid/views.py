import base64
import sendgrid
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import RedirectView
from django.http import Http404
from django.core.urlresolvers import reverse_lazy
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.contrib import messages
from django.conf import settings
from sendgrid.helpers.mail import Email, Content, Mail, Personalization, Attachment
from braces import views

from .models import List
from .models import Person
from .models import Template

from . import forms


class RestrictToOwnerMixin(views.LoginRequiredMixin):
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class SendEmailView(
        views.LoginRequiredMixin,
        RedirectView):

    model = Template

    def __init__(self, **kwargs):
        self.sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)

        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_redirect_url(self, *args, **kwargs):
        return reverse('grid:people_detail', kwargs={'slug': self.person.slug})

    def get_object(self, tp_pk):
        try:
            template = self.model.objects.get(
                    lists__pk=tp_pk,
                    user=self.request.user
                    )
        except Template.DoesNotExist:
            raise Http404
        else:
            return template

    def get_person(self, to_pk, tp_pk):
        try:
            person = Person.objects.get(
                    pk=to_pk,
                    lists_id__pk=tp_pk,
                    user=self.request.user
                    )
        except Person.DoesNotExist:
            raise Http404
        else:
            return person

    def render_body(self, to):
        f = open(self.template.template_email.path)
        body = ""

        for line in f:
            body += line.replace('{{TO}}', to)
        f.close()

        return body

    def attach_file(self):
        attachment = Attachment()
        with open(self.template.attachment.path, "rb") as f:
            attachment.set_content(base64.b64encode(f.read()))
            attachment.set_type("application/pdf")
            attachment.set_filename(self.template.slug+".pdf")
            attachment.set_disposition("attachment")
            attachment.set_content_id(self.template.title)

        return attachment

    def get(self, request, *args, **kwargs):
        self.template = self.get_object(kwargs.get('tp_pk'))
        self.person = self.get_person(kwargs.get('to_pk'), kwargs.get('tp_pk'))

        mail = Mail()
        mail.set_from(Email(self.request.user.email))
        mail.set_subject(self.template.title)

        personalization = Personalization()
        personalization.add_to(Email(self.person.email))
        mail.add_personalization(personalization)

        body = self.render_body(self.person.name)
        mail.add_content(Content("text/html", body))

        if self.template.attachment:
            mail.add_attachment(self.attach_file())

        self.sg.client.mail.send.post(request_body=mail.get())
        messages.info(
            request,
            """You have just send an email to <strong>{0.email}</strong>
            with the subject <strong>{1}</strong>
            """
            .format(self.person, self.template.title))

        return super(SendEmailView, self).get(request, *args, **kwargs)


class ListListView(
        RestrictToOwnerMixin,
        ListView):

    model = List

    def get_queryset(self):
        queryset = super(ListListView, self).get_queryset()
        queryset = queryset.annotate(contact_count=Count('contacts'))
        return queryset


class ListCreateView(
        views.LoginRequiredMixin,
        views.SetHeadlineMixin,
        CreateView):

    headline = 'Create'
    form_class = forms.ListForm
    model = List

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(ListCreateView, self).form_valid(form)


class ListUpdateView(
        RestrictToOwnerMixin,
        views.SetHeadlineMixin,
        UpdateView):

    headline = 'Edit'
    form_class = forms.ListForm
    model = List


class PersonRemoveView(
        views.LoginRequiredMixin,
        RedirectView):

    model = Person

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('grid:home')

    def get_object(self, pk, lists_pk):
        try:
            person = self.model.objects.get(
                    pk=pk,
                    user=self.request.user
                    )
        except List.DoesNotExist:
            raise Http404
        else:
            return person

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(kwargs.get('pk'), kwargs.get('lists_pk'))
        self.list = self.object.lists_id
        messages.warning(
                request,
                """
                <strong>{0.email}</strong> was removed from your contacts
                """.format(self.object))
        self.object.delete()
        return super(PersonRemoveView, self).get(request, *args, **kwargs)


class PersonListView(
        RestrictToOwnerMixin,
        ListView):

    model = Person
    paginate_by = 25

    def get_queryset(self):
        queryset = super(PersonListView, self).get_queryset()
        queryset = queryset.filter(lists_id__slug=self.kwargs['lists_id'])
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(PersonListView, self).get_context_data(*args, **kwargs)
        context['list_slug'] = self.kwargs['lists_id']
        return context


class PersonDetailView(
        RestrictToOwnerMixin,
        DetailView):

    model = Person


class PersonCreateView(
        views.LoginRequiredMixin,
        views.SetHeadlineMixin,
        CreateView):

    headline = 'Create'
    form_class = forms.PersonForm
    model = Person

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(PersonCreateView, self).form_valid(form)


class PersonUpdateView(
        RestrictToOwnerMixin,
        views.SetHeadlineMixin,
        UpdateView):

    headline = 'Edit'
    form_class = forms.PersonForm
    model = Person


class TemplateListView(
        RestrictToOwnerMixin,
        ListView):

    model = Template
    paginate_by = 25


class TemplateDetailView(
        RestrictToOwnerMixin,
        DetailView):

    model = Template


class TemplateCreateView(
        views.LoginRequiredMixin,
        views.SetHeadlineMixin,
        CreateView):

    headline = 'Create'
    form_class = forms.TemplateForm
    model = Template

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(TemplateCreateView, self).form_valid(form)


class TemplateUpdateView(
        RestrictToOwnerMixin,
        views.SetHeadlineMixin,
        UpdateView):

    headline = 'Edit'
    form_class = forms.TemplateForm
    model = Template
