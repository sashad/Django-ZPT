from django.urls import path

from . import views

urlpatterns = [
	path('file', views.from_file, name='from_file'),
	path('string', views.from_string, name='from_string'),
]
