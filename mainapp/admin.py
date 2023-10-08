from django.contrib import admin

from mainapp.models import Stamp, StampGroup

# @admin.register(Group)
# class PostAdmin(admin.ModelAdmin):
#     list_display = ('title', 'slug',)
#     search_fields = ('title', 'slug',)
#     empty_value_display = '-пусто-'

admin.site.register(StampGroup)
admin.site.register(Stamp)
