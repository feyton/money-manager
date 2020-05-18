from django.urls import path
from rest_framework import routers

from .views import home_view, user_view, UserViewSet, GroupViewSet, notification_view, task_completed_view, complete_task

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

urlpatterns = [
    path('', home_view, name='home'),
    path('profile/', user_view, name='profile'),
    path('notification', notification_view, name='notification'),
    path('task-completed/<pk>/', task_completed_view, name='task-completed'),
    path('complete-task/<pk>/', complete_task, name='complete')
]
