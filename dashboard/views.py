from .data import data
import random
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import get_template, render_to_string
from django.utils.decorators import method_decorator
from django.views.generic import ListView, View
from rest_framework import authentication, permissions, viewsets
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import UserProfile

from .forms import (AddAccountForm, AddTaskForm, AddTransactionForm,
                    AddWorkerForm, UpdateProfileForm, UpdateUserForm, AccountTransferForm, AccountTransfer)
from .models import Employee, Task, Transaction, Account
from .serializers import GroupSerializer, UserSerializer
from .utils import generate_pdf_weasy

User = get_user_model()


@method_decorator(login_required, name='dispatch')
class HomeView(View):
    def get(self, *args, **kwargs):
        template_name = 'index.html'
        form = AddTaskForm
        add_worker = AddWorkerForm()
        tasks = Task.objects.filter(user=self.request.user, completed=False)
        workers = Employee.objects.filter(
            manager=self.request.user, on_payroll=True)
        context = {
            'active': 'home',
            'form': form,
            'tasks': tasks,
            'workers': workers,
            'add_worker_form': add_worker
        }

        return render(self.request, template_name, context)

    def post(self, *args, **kwargs):
        form = AddTaskForm(self.request.POST or None)
        add_worker_form = AddWorkerForm(self.request.POST or None)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = self.request.user
            task.save()
            messages.info(self.request, 'Task Added Successfully')
            return redirect('dashboard:home')
        elif add_worker_form.is_valid():
            worker = add_worker_form.save(commit=False)
            worker.manager = self.request.user
            worker.save()
            messages.info(self.request, 'New worker added successfully')
            return redirect('dashboard:home')
        messages.error(self.request, 'Fill the form correctly')
        return render(self.request, 'index.html', {'form': form, 'add_worker_form': add_worker_form})


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
@method_decorator(login_required, name='dispatch')
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


@method_decorator(login_required, name='dispatch')
class TransactionView(View):
    def get(self, *args, **kwargs):
        transactions = Transaction.objects.all().order_by('-date_created')
        form = AddTransactionForm
        template = 'pages/tables.html'
        context = {
            'active': 'transaction',
            'transactions': transactions,
            'form': form
        }
        return render(self.request, template, context)

    def post(self, *args, **kwargs):
        form = AddTransactionForm(self.request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(
                self.request, 'New Transaction recorded succesfully')
            return redirect('dashboard:transaction')
        messages.error(self.request, 'Fill the form')
        return redirect('dashboard:transaction')


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


def generate_pdf(request):
    template = 'pdf.html'
    donation = get_object_or_404(Transaction, ref_number='5-2020-05-20-FUYF6')
    context = {
        'transaction': donation
    }
    file_name = '%s-%s' % (donation.ref_number, donation.amount)

    pdf = generate_pdf_weasy(request, template, file_name, context)
    return pdf


def edit_transaction(request, pk):
    transaction = get_object_or_404(Transaction, id=pk)
    transaction_amount = transaction.amount
    transaction_category = transaction.category.name
    form = AddTransactionForm(instance=transaction)
    context = {
        'form': form,
        'active': 'transaction'
    }
    template = 'pages/change_transaction.html'
    if request.method == 'POST':
        form = AddTransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            if 'amount' in form.changed_data:
                new_amount = form.cleaned_data.get('amount')

                account = transaction.account
                if transaction.category.name == 'Income':
                    account.available_balance -= transaction_amount
                    account.available_balance += new_amount
                    account.save()
                    messages.info(
                        request, '%s account has been updated' % (account.name))
                elif transaction.category.name == 'Expense':
                    account.available_balance += transaction_amount
                    account.available_balance -= new_amount
                    account.save()
                    messages.info(request, '%s Account updated' %
                                  (account.name))
            form.save()
            # print(request)
            return redirect('dashboard:transaction')
        messages.error(request, 'Errors in the form')
        return render(request, template, context)
    return render(request, template, context)


class AccountsView(View):
    def get(self, *args, **kwargs):
        form = AccountTransferForm
        template = 'pages/accounts.html'
        accounts = Account.objects.all()
        context = {'active': 'accounts',
                   'accounts': accounts,
                   'form': form}

        return render(self.request, template, context)

    def post(self, *args, **kwargs):
        form = AccountTransferForm(self.request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(self.request, 'Transfer completed successfully')
            return redirect('dashboard:accounts-view')

        messages.error(self.request, 'Form not valid')
        return redirect('dashboard:accounts-view')

account_view = AccountsView.as_view()


def edit_account(request, pk):
    acc = get_object_or_404(Account, id=pk)
    if acc:
        form = AddAccountForm(instance=acc)
        context= {
            'account': acc,
            'form': form,
            'active': 'accounts',
            'obj_name': acc.name
        }

        if request.method == 'POST':
            form = AddAccountForm(request.POST, instance=acc)
            if form.is_valid():
                form.save()
                messages.info(request, '%s account updated successfully' %(acc.name))
                return redirect('dashboard:accounts-view')
            messages.error(request, 'Error in form')
            context ={
                'active': 'accounts',
                'form': form,
                'obj_name': acc.name   
            }
            return render(request, 'pages/change_transaction.html', context)
        return render(request, 'pages/change_transaction.html', context)