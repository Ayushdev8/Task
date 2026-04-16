from django.urls import path
from . import views
urlpatterns =[
    path('api/register/',views.RegisterView.as_view(), name= "apiregister"),
    path('api/tasks/<int:pk>/', views.UpdateTaskView.as_view(), name='task-detail'),
    path('api/tasks/', views.AddTaskView.as_view(),name="task-created"),
    path('api/taskdelete/<int:pk>/',views.TaskdeleteView.as_view(),name="task-delete"),
    path('api/user/',views.UserDetailView.as_view(),name="get-user"),
    path("api/total-task/",views.TotalTaskView.as_view(),name="totaltask"),

]