from django import forms
from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django_ckeditor_5.widgets import CKEditor5Widget


class FlatPageForm(forms.ModelForm):
    class Meta:
        model = FlatPage
        fields = "__all__"
        widgets = {
            "content": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="extends"
            )
        }


class FlatPageAdminCustom(FlatPageAdmin):
    form = FlatPageForm


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdminCustom)
