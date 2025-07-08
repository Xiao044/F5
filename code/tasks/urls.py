from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('task_square/', views.task_square, name='task_square'),
    path('team_collaboration/', views.team_collaboration, name='team_collaboration'),
    path('study_partner/', views.study_partner, name='study_partner'),
    path('ranking/', views.ranking, name='ranking'),
    path('data_statistics/', views.data_statistics, name='data_statistics'),
    path('add_task/', views.add_task, name='add_task'),
    path('login/', views.login, name='login'),
    path('chat_assistant/', views.chat_assistant, name='chat_assistant'),
]