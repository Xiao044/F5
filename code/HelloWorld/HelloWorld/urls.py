from django.contrib import admin
from django.urls import path
from tasks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # 任务列表页面
    path('', views.task_list, name='task_list'), 
    # 删除任务页面
    path('delete/<int:pk>/', views.delete_task, name='delete_task'),  
    # 完成任务页面
    path('complete/<int:pk>/', views.complete_task, name='complete_task'),  
    # 任务详情页面
    path('task_detail/', views.task_detail, name='task_detail'),  
]   