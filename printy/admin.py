from django.contrib import admin

from mainapp.admin import StampAdmin, StampGroupAdmin
from printy.models import Printy, PrintyGroup


@admin.register(PrintyGroup)
class PrintyGroupAdmin(StampGroupAdmin):
    pass


@admin.register(Printy)
class PrintyAdmin(StampAdmin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.remove("printy")
