from django.contrib import messages
from django.core import serializers
from django.shortcuts import render
from rest_framework import authentication, permissions, viewsets
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from dashboard.models import Account, Transaction


class AccountSummary(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        labels = []
        data_set = []
        for account in Account.objects.all():
            labels.append(account.name)
            data_set.append(account.available_balance)
        data = {
            'labels': labels,
            'chart_data': data_set
        }

        return Response(data)


account_api_call = AccountSummary.as_view()


class MessagesGet(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        mess = messages.get_messages(self.request)
        if mess:
            message = []
            for m in mess:
                message.append(str(m))

            data = {

                'message': message
            }
            return Response(message)
        data = {
            'No message': 'True'
        }
        return Response(data)


messages_api_call = MessagesGet.as_view()


class BigChartData(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        data_set_1 = [65, 59, 80, 81, 56, 55, 40 ,60, 60, 55, 30, 78, 100]
        data_set_2 = [30, 20, 60, 95, 64, 78, 90, 80, 90, 70, 40, 70, 89]
        data = {
            'label': labels,
            'income': data_set_1,
            'expense': data_set_2
        }
        return Response(data)


big_chart_data = BigChartData.as_view()


class MainDashboardChart(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        data = {
            'labels': labels
        }
        return Response(data)

main_dashboard_chart_data = MainDashboardChart.as_view()