from django import forms
from user.models import User, UserProfile
from .models import Task, Transaction, Account, Employee
from bootstrap_datepicker_plus import DateTimePickerInput

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image', 'biography']
        widgets = {
            'biography': forms.Textarea(attrs={'rows': 3, 'cols': 60}),
        }


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class AddTaskForm(forms.ModelForm):
    class Meta:
        model=Task
        exclude=['user', ]
        widgets={
            'action': forms.Textarea(attrs={'class': 'form-control'}),
            'deadline': DateTimePickerInput()
        }


class AddTransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        exclude = ['ref_number',]
        required_css_class = 'required'

class AddWorkerForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ['manager', ]

class AddAccountForm(forms.ModelForm):
    class Meta:
        model = Account
        exclude = ['available_balance', 'transactions']