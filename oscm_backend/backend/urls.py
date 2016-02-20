from django.conf.urls import url
from backend.views import *

urlpatterns = [
    url(r'^put/', PutAPIView.as_view()),
    url(r'^get/', GetAPIView.as_view()),
    url(r'^search/', SearchAPIView.as_view()),
]
