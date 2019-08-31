from django.urls import path

from . import views
from .views import HomePageView

urlpatterns = [
    path('', views.index, name='index'),
    path('home', HomePageView.as_view(), name='home'),
    path('getElevator', views.index, name='index'),

]