from django.urls import path

from apps.share import views

urlpatterns = [
    path("", views.TTT.as_view()),
    path("s/", views.tests),
]
