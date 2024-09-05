from django.urls import path

from . import views

app_name = 'testing'

urlpatterns = [
    path('', views.index, name='index'),
    path('brackets/', views.brackets, name='brackets'),
    path('bj/', views.bj, name='bj'),
    path('neighbours/', views.neighbours, name='neighbours'),
    path('series/', views.series, name='series'),
]