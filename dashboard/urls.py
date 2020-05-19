from django.urls import path
from rest_framework import routers

from .views import (GroupViewSet, UserViewSet, complete_task,
                    delete_transaction, home_view, notification_view,
                    task_completed_view, transaction_view, user_view, pay_worker_view)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

urlpatterns = [
    path('', home_view, name='home'),
    path('profile/', user_view, name='profile'),
    path('notification', notification_view, name='notification'),
    path('task-completed/<pk>/', task_completed_view, name='task-completed'),
    path('complete-task/<pk>/', complete_task, name='complete'),
    path('transaction/', transaction_view, name='transaction'),
    path('delete-transaction/<pk>/', delete_transaction, name="delete-transaction"),
    path('pay-worker/<pk>/', pay_worker_view, name='pay-worker')
]
