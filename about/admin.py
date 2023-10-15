from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin

from about.models import Contact, ContactYandexMap

admin.site.register(ContactYandexMap)


class PostAdminForm(forms.ModelForm):
    contants = forms.CharField(widget=CKEditorUploadingWidget())
    links = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Contact
        fields = "__all__"


class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm


admin.site.register(Contact, PostAdmin)
