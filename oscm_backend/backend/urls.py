from django.conf.urls import url
from backend.views import *

urlpatterns = [
    url(r'^push/', PushAPIView.as_view()),
    url(r'^pull/', PullAPIView.as_view()),
    url(r'^search/', SearchAPIView.as_view()),
]
