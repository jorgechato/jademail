from __future__ import unicode_literals
import os

from django.db import models
from ckeditor.fields import RichTextField
from django.core.urlresolvers import reverse
from slugify import slugify


def content_file_name(instance, filename):
    ext = filename.split('.')[-1]
    slug = slugify(instance.title)
    filename = "{}.{}".format(slug, ext)
    return os.path.join('grid', filename)


class List(models.Model):
    title = models.CharField(max_length=240)
    description = models.CharField(max_length=240)
    slug = models.SlugField(max_length=240, blank=True, editable=False)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return unicode(self.slug)

    def save(self, *arg, **kwargs):
        self.slug = slugify(self.email)
        super(List, self).save(*arg, **kwargs)

    def get_absolute_url(self):
        return reverse('grid:list_detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ('title',)


class Person(models.Model):
    name = models.CharField(max_length=240)
    last_name = models.CharField(max_length=240, blank=True)
    email = models.EmailField(max_length=240, unique=True)
    mobile = models.CharField(max_length=240, blank=True)
    web = models.URLField(max_length=240, blank=True)
    linked_in = models.URLField(max_length=240, blank=True)
    facebook = models.URLField(max_length=240, blank=True)
    lists_id = models.ManyToManyField(List, blank=True)
    street = models.CharField(max_length=500, blank=True)
    email_sent = models.BooleanField(default=False, editable=False)
    slug = models.SlugField(max_length=240, blank=True, editable=False)

    def __str__(self):
        return "{}, {}".format(self.last_name, self.name)

    def __unicode__(self):
        return unicode(self.slug)

    def save(self, *arg, **kwargs):
        self.slug = slugify(self.email)
        super(Person, self).save(*arg, **kwargs)

    def get_absolute_url(self):
        return reverse('grid:people_detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ('last_name', 'name')


class Comment(models.Model):
    title = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    content = RichTextField()
    person_id = models.ForeignKey(Person, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created_at',)


class Template(models.Model):
    title = models.CharField(max_length=140, unique=True)
    content = RichTextField()
    template_file = models.FileField(upload_to=content_file_name, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=240, blank=True, editable=False)

    def __unicode__(self):
        return unicode(self.slug)

    def save(self, *arg, **kwargs):
        self.slug = slugify(self.title)
        super(Template, self).save(*arg, **kwargs)

    def get_absolute_url(self):
        return reverse('grid:template_detail', kwargs={'slug': self.slug})
