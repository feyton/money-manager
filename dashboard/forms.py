from django import forms
from user.models import User, UserProfile
from .models import Task
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
        exclude=['user', 'deadline']
        widgets={
            'action': forms.Textarea(attrs={'class': 'form-control'}),
            'deadline': DateTimePickerInput()
        }
