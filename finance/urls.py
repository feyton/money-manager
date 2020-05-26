from django.urls import path
from . import views


urlpatterns = [
    path('account/', views.account_api_call, name='account-chart-data'),
    path('messages/', views.messages_api_call, name = 'messages-call'),
    path('expense/', views.big_chart_data, name='big-chart-data'),
    path('main-dashboard/', views.main_dashboard_chart_data, name='main-dashboard-chart'),
    path('user/', views.user_view, name='user-view-flutter')
]