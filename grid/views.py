import base64
import sendgrid
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import RedirectView
from django.http import Http404
from django.core.urlresolvers import reverse_lazy
from django.db.models import Count
from django.contrib import messages
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from sendgrid.helpers.mail import Email, Content, Mail, Personalization, Attachment
from braces import views
from slugify import slugify

from .models import List
from .models import Person
from .models import Template

from . import forms


class RestrictToOwnerMixin(views.LoginRequiredMixin):
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class EmailParse():

    def render_body(self, to, path):
        f = open(path)
        body = ""

        for line in f:
            body += line.replace('{{TO}}', to)
        f.close()

        return body

    def attach_file(self, f, ext, slug, title):
        attachment = Attachment()
        attachment.set_content(base64.b64encode(f.read()))
        attachment.set_type("application/"+ext)
        attachment.set_filename(slug+"."+ext)
        attachment.set_disposition("attachment")
        attachment.set_content_id(title)

        return attachment


class SendEmailView(
        views.LoginRequiredMixin,
        EmailParse,
        RedirectView):

    model = Template

    def __init__(self, **kwargs):
        self.sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)

        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('grid:people_detail',
                kwargs={'slug': self.person.slug}) + "?q=" + kwargs.get('tp_pk')

    def get_object(self, tp_pk):
        try:
            template = self.model.objects.get(
                    lists__slug=tp_pk,
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
                    lists_id__slug=tp_pk,
                    user=self.request.user
                    )
        except Person.DoesNotExist:
            raise Http404
        else:
            return person

    def get(self, request, *args, **kwargs):
        self.template = self.get_object(kwargs.get('tp_pk'))
        self.person = self.get_person(kwargs.get('to_pk'), kwargs.get('tp_pk'))

        mail = Mail()
        mail.set_from(Email(self.request.user.email))
        mail.set_subject(self.template.title)

        personalization = Personalization()
        personalization.add_to(Email(self.person.email))
        mail.add_personalization(personalization)

        body = self.render_body(self.person.name, self.template.template_email.path)
        mail.add_content(Content("text/html", body))

        if self.template.attachment:
            path = self.template.attachment.path
            ext = path.split('.')[-1]
            with open(path, "rb") as f:
                mail.add_attachment(self.attach_file(
                    f, ext, self.template.slug, self.template.title))

        self.sg.client.mail.send.post(request_body=mail.get())
        messages.info(
            request,
            """You have just send an email to <strong>{0.email}</strong>
            with the subject <strong>{1}</strong>
            """
            .format(self.person, self.template.title))

        self.person.email_sent = True
        self.person.save()

        return super(SendEmailView, self).get(request, *args, **kwargs)


class ListListView(
        RestrictToOwnerMixin,
        views.SetHeadlineMixin,
        ListView):

    model = List
    headline = 'Lists'
    paginate_by = 25

    def get_queryset(self):
        queryset = super(ListListView, self).get_queryset()
        queryset = queryset.annotate(contact_count=Count('contacts'))
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(ListListView, self).get_context_data(*args, **kwargs)
        context['path'] = reverse_lazy('grid:list_create')
        context['active_tab'] = 'list'
        return context


class ListCreateView(
        views.LoginRequiredMixin,
        views.SetHeadlineMixin,
        views.FormMessagesMixin,
        CreateView):

    headline = 'Create a new list'
    form_class = forms.ListForm
    model = List
    form_invalid_message = _(u'There was an error in the process')

    def get_form_kwargs(self):
        kwargs = super(ListCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_form_valid_message(self):
        return u"""You have just <strong>{0}</strong> the list
               <strong>{1.title}</strong> successfully
               """.format(self.headline, self.object)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(ListCreateView, self).form_valid(form)


class ListUpdateView(
        RestrictToOwnerMixin,
        views.SetHeadlineMixin,
        views.FormMessagesMixin,
        UpdateView):

    headline = 'Edit'
    form_class = forms.ListForm
    model = List
    form_invalid_message = _(u'There was an error in the process')

    def get_form_valid_message(self):
        return u"""You have just <strong>{0}</strong> the list
               <strong>{1.title}</strong> successfully
               """.format(self.headline, self.object)

    def get_form_kwargs(self):
        kwargs = super(ListUpdateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


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
        except Person.DoesNotExist:
            raise Http404
        else:
            return person

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(kwargs.get('pk'), kwargs.get('lists_pk'))
        self.list = self.object.lists_id
        messages.warning(
                request,
                """
                The contact <strong>{0.email}</strong> was removed from
                your contacts
                """.format(self.object))
        self.object.delete()
        return super(PersonRemoveView, self).get(request, *args, **kwargs)


class PersonListView(
        RestrictToOwnerMixin,
        views.SetHeadlineMixin,
        ListView):

    model = Person
    paginate_by = 25
    headline = 'Contacts from'

    def get_queryset(self):
        queryset = super(PersonListView, self).get_queryset()
        queryset = queryset.filter(lists_id__slug=self.kwargs['lists_id'])
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(PersonListView, self).get_context_data(*args, **kwargs)
        context['list_slug'] = self.kwargs['lists_id']
        context['path'] = reverse_lazy('grid:people_create')
        return context


class PersonDetailView(
        RestrictToOwnerMixin,
        DetailView):

    model = Person

    def get_context_data(self, *args, **kwargs):
        context = super(PersonDetailView, self).get_context_data(*args, **kwargs)
        context['q'] = self.request.GET.get('q')
        return context


class PersonCreateView(
        views.LoginRequiredMixin,
        views.SetHeadlineMixin,
        views.FormMessagesMixin,
        CreateView):

    headline = 'Create a new contact'
    form_class = forms.PersonForm
    model = Person
    form_invalid_message = _(u'There was an error in the process')
    success_url = reverse_lazy('grid:home')

    def get_form_valid_message(self):
        return u"""You have just <strong>{0}</strong> the contact
               <strong>{1.email}</strong> successfully
               """.format(self.headline, self.object)

    def get_form_kwargs(self):
        kwargs = super(PersonCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(PersonCreateView, self).form_valid(form)


class PersonUpdateView(
        RestrictToOwnerMixin,
        views.SetHeadlineMixin,
        views.FormMessagesMixin,
        UpdateView):

    headline = 'Edit'
    form_class = forms.PersonForm
    model = Person
    form_invalid_message = _(u'There was an error in the process')
    success_url = reverse_lazy('grid:home')

    def get_form_valid_message(self):
        return u"""You have just <strong>{0}</strong> the contact
               <strong>{1.email}</strong> successfully
               """.format(self.headline, self.object)

    def get_form_kwargs(self):
        kwargs = super(PersonUpdateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class TemplateListView(
        RestrictToOwnerMixin,
        views.SetHeadlineMixin,
        ListView):

    model = Template
    paginate_by = 25
    headline = 'Templates'

    def get_context_data(self, *args, **kwargs):
        context = super(TemplateListView, self).get_context_data(*args, **kwargs)
        context['path'] = reverse_lazy('grid:template_create')
        context['active_tab'] = 'template'
        return context

    def get_queryset(self):
        queryset = super(TemplateListView, self).get_queryset()
        queryset = queryset.annotate(list_count=Count('lists'))
        return queryset


class TemplateDetailView(
        RestrictToOwnerMixin,
        DetailView):

    model = Template


class TemplateCreateView(
        views.LoginRequiredMixin,
        views.SetHeadlineMixin,
        views.FormMessagesMixin,
        CreateView):

    headline = 'Create a new template'
    form_class = forms.TemplateForm
    model = Template
    form_invalid_message = _(u'There was an error in the process')

    def get_form_valid_message(self):
        return u"""You have just <strong>{0}</strong> the template
               <strong>{1.title}</strong> successfully
               """.format(self.headline, self.object)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(TemplateCreateView, self).form_valid(form)


class TemplateUpdateView(
        RestrictToOwnerMixin,
        views.SetHeadlineMixin,
        views.FormMessagesMixin,
        UpdateView):

    headline = 'Edit'
    form_class = forms.TemplateForm
    model = Template
    form_invalid_message = _(u'There was an error in the process')

    def get_form_valid_message(self):
        return u"""You have just <strong>{0}</strong> the template
               <strong>{1.title}</strong> successfully
               """.format(self.headline, self.object)


class CustomEmailView(
        views.LoginRequiredMixin,
        views.FormMessagesMixin,
        views.SetHeadlineMixin,
        EmailParse,
        FormView):

    headline = 'Send a custom message'
    form_class = forms.EmailForm
    template_name = "email_form.html"
    form_invalid_message = _(u'There was an error in the process')
    success_url = reverse_lazy('grid:custom_email')

    def __init__(self, **kwargs):
        self.sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)

        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_context_data(self, *args, **kwargs):
        context = super(CustomEmailView, self).get_context_data(*args, **kwargs)
        context['active_tab'] = 'email'
        return context

    def get_form_kwargs(self):
        kwargs = super(CustomEmailView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_form_valid_message(self):
        return u"""You have just send an email to <strong>{}</strong>
               with the subject <strong>{}</strong>
               """.format(self.email, self.subject)

    def render_content(self, text, content, title):
        return text.replace('{{TITLE}}', title).replace('{{CONTENT}}', content)

    def form_valid(self, form):
        self.template = form.cleaned_data['template']
        self.email = form.cleaned_data['email']
        self.subject = form.cleaned_data['subject']

        mail = Mail()
        mail.set_from(Email(self.request.user.email))
        mail.set_subject(self.subject)

        personalization = Personalization()
        personalization.add_to(Email(self.email))
        mail.add_personalization(personalization)

        body_personalized = self.render_body(
                form.cleaned_data['name'],
                self.template.template_file.path)
        body = self.render_content(
                body_personalized,
                form.cleaned_data['content'],
                self.subject)
        mail.add_content(Content("text/html", body))

        if form.cleaned_data['attachment']:
            file_name = form.cleaned_data['attachment'].name
            ext = file_name.split('.')[-1]
            with form.cleaned_data['attachment'] as f:
                mail.add_attachment(self.attach_file(
                    f, ext,
                    slugify(file_name),
                    self.subject))

        self.sg.client.mail.send.post(request_body=mail.get())

        return super(CustomEmailView, self).form_valid(form)
