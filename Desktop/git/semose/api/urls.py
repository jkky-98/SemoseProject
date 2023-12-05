from django.urls import path
from . import views

urlpatterns = [
    path('', views.index2),
    path('end', views.DataView.as_view()),
    path('zicbang', views.ZicbangServe),
    path('info', views.InfoView.as_view()),
]