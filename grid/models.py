from __future__ import unicode_literals
import os

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField
from django.core.urlresolvers import reverse
from slugify import slugify
from django.core.files.base import ContentFile


def content_file_name(instance, filename, prefix=""):
    ext = filename.split('.')[-1]
    slug = slugify(instance.title)
    filename = "{}{}.{}".format(slug, prefix, ext)
    return os.path.join('grid', filename)


class Template(models.Model):
    title = models.CharField(max_length=140, unique=True)
    content = RichTextField()
    template_file = models.FileField(upload_to=content_file_name)
    attachment = models.FileField(upload_to=content_file_name, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=340, blank=True, editable=False)
    user = models.ForeignKey(User, related_name='templates', on_delete=models.CASCADE)
    template_email = models.FileField(blank=True, editable=False)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return unicode(self.slug) or unicode(self.template_email)

    def save(self, *arg, **kwargs):
        self.slug = slugify(self.title)
        self.template_email.delete(save=False)

        f = self.template_file.file
        template = ""

        for line in f:
            template += line.replace('{{TITLE}}', self.title).replace('{{CONTENT}}', self.content)

        self.template_email = ContentFile(template)
        self.template_email.name = content_file_name(self, self.template_file.name, ".body")

        super(Template, self).save(*arg, **kwargs)

    def get_absolute_url(self):
        return reverse('grid:template_detail', kwargs={'slug': self.slug})

    class Meta:
        unique_together = ('title', 'user')


class List(models.Model):
    title = models.CharField(max_length=240)
    description = models.CharField(max_length=240, blank=True)
    slug = models.SlugField(max_length=340, blank=True, editable=False)
    user = models.ForeignKey(User, related_name='lists', on_delete=models.CASCADE)
    template = models.ForeignKey(Template, related_name='lists')

    def __str__(self):
        return self.title

    def __unicode__(self):
        return unicode(self.slug)

    def save(self, *arg, **kwargs):
        self.slug = slugify(self.title)
        super(List, self).save(*arg, **kwargs)

    def get_absolute_url(self):
        return reverse('grid:list_detail', kwargs={'lists_id': self.slug})

    class Meta:
        ordering = ('title',)
        unique_together = ('title', 'user')


class Person(models.Model):
    name = models.CharField(max_length=240)
    last_name = models.CharField(max_length=240, blank=True)
    email = models.EmailField(max_length=240, unique=True)
    mobile = models.CharField(max_length=240, blank=True)
    web = models.URLField(max_length=240, blank=True)
    linked_in = models.URLField(max_length=240, blank=True)
    facebook = models.URLField(max_length=240, blank=True)
    street = models.CharField(max_length=500, blank=True)
    email_sent = models.BooleanField(default=False, editable=False)
    slug = models.SlugField(max_length=340, blank=True, editable=False)
    lists_id = models.ManyToManyField(List, related_name='contacts')
    user = models.ForeignKey(User, related_name='contacts', on_delete=models.CASCADE)

    def __str__(self):
        return "{}: {}".format(self.name, self.email)

    def __unicode__(self):
        return unicode(self.slug)

    def save(self, *arg, **kwargs):
        self.slug = slugify(self.email)
        super(Person, self).save(*arg, **kwargs)

    def get_absolute_url(self):
        return reverse('grid:people_detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ('last_name', 'name')
        unique_together = ('email', 'user')


class Comment(models.Model):
    title = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    content = RichTextField()
    person_id = models.ForeignKey(Person, related_name='comments', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created_at',)
