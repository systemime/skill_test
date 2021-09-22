from django.urls import path

from apps.share import views

urlpatterns = [path("", views.test)]
