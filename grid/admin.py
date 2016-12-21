from django import forms
from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from ckeditor.widgets import CKEditorWidget

from .models import List
from .models import Person
from .models import Comment
from .models import Template


class CommentAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Comment
        fields = "__all__"


class CommentAdmin(ImportExportActionModelAdmin):
    form = CommentAdminForm

    list_display = ('user', 'title', 'created_at', 'get_content')
    readonly_fields = ('created_at',)
    list_filter = ('person_id', 'title')
    list_display_links = ('title',)
    search_fields = ('title', 'content')
    ordering = ('-created_at', 'title')
    raw_id_fields = ('person_id',)

    def get_content(self, obj):
        return obj.content

    get_content.allow_tags = True


class CommentInline(admin.StackedInline):
    model = Comment
    readonly_fields = ('created_at', 'person_id',)
    extra = 1


class PersonAdmin(ImportExportActionModelAdmin):
    list_display = ('user', 'email', 'name', 'last_name', 'mobile', 'web',
            'linked_in', 'facebook', 'email_sent')
    list_filter = ('name', 'last_name', 'lists_id')
    list_display_links = ('name', 'email')
    search_fields = ('name', 'last_name', 'email')
    inlines = (CommentInline,)
    ordering = ('name', 'last_name', 'email')
    filter_horizontal = ('lists_id',)


class ListAdmin(ImportExportActionModelAdmin):
    list_display = ('user', 'title', 'description', 'template')
    list_filter = ('title',)
    list_display_links = ('title',)
    search_fields = ('title',)
    ordering = ('title', 'description')


class TemplateAdmin(ImportExportActionModelAdmin):
    list_display = ('user', 'title', 'template_file', 'template_email', 'created_at')
    list_filter = ('title',)
    list_display_links = ('title',)
    search_fields = ('title',)
    ordering = ('title',)


admin.site.register(List, ListAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Template, TemplateAdmin)
