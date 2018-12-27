from django.conf.urls import  url
import views

urlpatterns = [
    url(r'^goto/(\w*)/?$', views.goto),
    url(r'^done/$', views.done),
]