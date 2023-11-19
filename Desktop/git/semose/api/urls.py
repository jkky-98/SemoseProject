from django.urls import path
from . import views
from .views import LogEntryView

urlpatterns = [
    path('', views.index2),
    path('end', views.DataView.as_view()),
    path('log', LogEntryView.as_view()),
]