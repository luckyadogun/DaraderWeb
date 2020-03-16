from django.urls import path, re_path

from .views import (HomePageView, SearchResultView)


urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
    path('search/', SearchResultView.as_view(), name="search"),
]
