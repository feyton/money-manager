from django.contrib import messages
from django.core import serializers
from django.shortcuts import render
from rest_framework import authentication, permissions, status, viewsets
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from dashboard.models import Account, Transaction
from dashboard.serializers import UserSerializer, GroupSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


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
        data_set_1 = [65, 59, 80, 81, 56, 55, 40, 60, 60, 55, 30, 78, 100]
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


class UserRecordView(APIView):
    """
    API View to create or get a list of all the registered
    users. GET request returns the registered users whereas
    a POST request allows to create a new user.
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                "error": True,
                "error_msg": serializer.error_messages,
            },
            status=status.HTTP_400_BAD_REQUEST
        )


user_view = UserRecordView.as_view()