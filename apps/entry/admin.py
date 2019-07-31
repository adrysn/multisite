from django.contrib import admin

from .models import Entry


class EntryAdmin(admin.ModelAdmin):

    list_display = ('title', 'created_at', 'modified_at',)
    list_filter = ('sites__name',)
    autocomplete_fields = ('sites',)


admin.site.register(Entry, EntryAdmin)
