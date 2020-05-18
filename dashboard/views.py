from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import View
from rest_framework import authentication, permissions, viewsets
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import UserProfile

from .forms import AddTaskForm, UpdateProfileForm, UpdateUserForm
from .models import Employee, Task
from .serializers import GroupSerializer, UserSerializer

User = get_user_model()


@method_decorator(login_required, name='dispatch')
class HomeView(View):
    def get(self, *args, **kwargs):
        template_name = 'index.html'
        form = AddTaskForm
        tasks = Task.objects.filter(user = self.request.user, completed=False)
        workers = Employee.objects.filter(manager=self.request.user)
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
        template = 'pages/notifications.html'
        return render(self.request, template)


notification_view = NotificationView.as_view()

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
        task.completed = True
        task.save()
        messages.success(request, 'Task completed')
        return redirect('dashboard:home')
    messages.error(request, 'No task with that ID')
    return redirect('dashboard:notification')
    
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
