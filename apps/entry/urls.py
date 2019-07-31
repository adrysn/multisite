from django.urls import path

from . import views


app_name = 'entries'

urlpatterns = [
    path('', views.EntryListView.as_view(), name='entry-list'),
]
