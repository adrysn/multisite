from django.views.generic import ListView

from .models import Entry


class EntryListView(ListView):
    """ Entry list view.

    Returns list of entries only belongs to the current site.
    """
    model = Entry
    template_name = 'entry/entry_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        queryset = Entry.on_site.all()  # all entries in the current site
        return queryset
