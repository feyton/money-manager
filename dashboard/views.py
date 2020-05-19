from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import View, ListView
from rest_framework import authentication, permissions, viewsets
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import UserProfile

from .forms import AddTaskForm, UpdateProfileForm, UpdateUserForm
from .models import Employee, Task, Transaction
from .serializers import GroupSerializer, UserSerializer

User = get_user_model()


@method_decorator(login_required, name='dispatch')
class HomeView(View):
    def get(self, *args, **kwargs):
        template_name = 'index.html'
        form = AddTaskForm
        tasks = Task.objects.filter(user = self.request.user, completed=False)
        workers = Employee.objects.filter(manager=self.request.user, on_payroll=True)
        context = {
            'active': 'home',
            'form': form,
            'tasks': tasks,
            'workers': workers
        }
        return render(self.request, template_name, context)

    def post(self, *args, **kwargs):
        form =AddTaskForm(self.request.POST or None)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = self.request.user
            task.save()
            messages.info(self.request, 'Task Added Successfully')
            return redirect('dashboard:notification')
        messages.info(self.request, 'Fill the form correctly')
        return redirect('dashboard:notification')


home_view = HomeView.as_view()


@method_decorator(login_required, name='dispatch')
class UserView(View):

    def get(self, *args, **kwargs):
        profile = UserProfile.objects.get(user=self.request.user)
        user_form = UpdateUserForm(instance=self.request.user)
        profile_form = UpdateProfileForm(
            instance=profile)

        template = 'pages/user.html'
        context = {
            'active': 'profile',
            'u_form': user_form,
            'p_form': profile_form
        }
        print(user_form)
        print(profile_form)
        return render(self.request, template, context)

    def post(self, *args, **kwargs):
        profile = UserProfile.objects.get(user=self.request.user)
        user_form = UpdateUserForm(
            self.request.POST or None, instance=self.request.user)
        profile_form = UpdateProfileForm(
            self.request.POST, self.request.FILES or None, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(self.request, 'Your profile has been updated')
            return redirect('dashboard:profile')
        messages.warning(self.request, 'Please fill the form correctly')
        return redirect('dashboard:profile')


user_view = UserView.as_view()

class NotificationView(View):
    def get(self, *args, **kwargs):
        tasks = Task.objects.filter(completed=True).count()
        context = {
            'active': 'notification',
            'tasks': tasks
        }
        template = 'pages/notifications.html'
        return render(self.request, template, context)


notification_view = NotificationView.as_view()

class TransactionView(View):
    def get(self, *args, **kwargs):
        transactions = Transaction.objects.all()
        template = 'pages/tables.html'
        context = {
            'active': 'transaction',
            'transactions': transactions
        }
        return render(self.request, template, context)

transaction_view = TransactionView.as_view()

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

def task_completed_view(request, pk):
    task = get_object_or_404(Task, id=pk)
    if task:
        task.delete()
        messages.success(request, 'Task deleted')
        return redirect('dashboard:home')
    messages.error(request, 'No task with that ID')
    return redirect('dashboard:home')
    
def complete_task(request, pk):
    task = get_object_or_404(Task, id=pk)
    if task:
        ref = task.ref_code
        task.completed = True
        task.save()
        data = {
            'message': 'Task completed',
            'ref': ref
        }
        return JsonResponse(data)

    else:
        data = {
            'message': 'No such task exist'
        }
        return JsonResponse(data)


def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, id=pk)
    if transaction:
        transaction.delete()
        messages.info(request, 'Transaction deleted successfully')
        return redirect('dashboard:transaction')

def pay_worker_view(request, pk):
    worker = get_object_or_404(Employee, id=pk)
    if worker:
        worker.pay()
        worker.save()
        messages.success(request, 'Employee payed successfully')
        return redirect('dashboard:home')

    else:
        messages.error(request, 'Something gone wrong')
        return redirect('dashboard:home')