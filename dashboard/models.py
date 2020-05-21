import random
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import post_save, pre_save, pre_delete
from django.contrib import messages

from .utils import ref_code_generator
tz = settings.TIME_ZONE

User = get_user_model()


def asset_code():
    month = datetime.now().month
    year = datetime.now().year
    number = random.randint(1000, 9000)

    return '%s-%s-%s' % (year, month, number)


def validate_purchase_date(value):
    if value > datetime.now().date():
        raise ValidationError('Purchase date cannot be in future')


def validate_deadline(value):
    if value <= timezone.now():
        raise ValidationError('Deadline must be in future')


def task_ref_code():
    date = datetime.now().month
    code = random.randint(1000, 9000)
    return '%s-%s' % (date, code)


class Asset(models.Model):
    code = models.CharField(blank=True, null=True, max_length=250, unique=True)
    name = models.CharField(max_length=250)
    purchase_price = models.PositiveIntegerField()
    depreciation_rate = models.FloatField()
    purchase_date = models.DateField(
        auto_now_add=False, null=True, blank=True, validators=[validate_purchase_date])

    class Meta:
        ordering = ['-purchase_price']

    def save(self, *args, **kwargs):
        if not self.code:
            code = asset_code()
            self.code = code
        super().save(*args, **kwargs)

    def __str__(self):
        return '%s-%s' % (self.code, self.name)

    def get_detail_url(self):
        return reverse('dashboard:detail', kwargs={'code': self.code})


class Employee(models.Model):
    # CHOICES
    statuses = (
        ('CON', 'Contract'),('CAS', 'Casual worker')
    )



    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name='Employee Name', blank=False)
    role = models.CharField(max_length=20, verbose_name='Employee Duties', blank=True, null=True)
    salary = models.PositiveIntegerField(verbose_name='Employee salary', blank=True, null=True)
    employment_type = models.CharField(max_length=3, blank=True, null=True, default='CAS', choices=statuses)
    city = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)

    start_date = models.DateField(auto_now=False, blank=True, null=True)
    recorded = models.DateTimeField(auto_now_add=True)
    payment_date = models.DateField(auto_now_add=False, verbose_name='Employee payment date')
    other_info = models.TextField()
    payment_account = models.ForeignKey('Account', on_delete=models.SET_NULL, null=True, blank=True)
    on_payroll = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
        ordering = ['salary']

    def __str__(self):
        return self.name

    def pay(self):
        account = self.payment_account
        if self.employment_type == 'CAS':
            account.available_balance -= self.salary
            self.on_payroll = False
            account.save()
        elif self.employment_type == 'CON':
            account.available_balance -= self.salary
            self.payment_date += timedelta(days=30)
            account.save()

    def pay_url(self):
        return reverse('dashboard:pay-worker', kwargs={'pk': self.id})



class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ref_code = models.CharField(
        max_length=100, blank=True, null=True)
    action = models.TextField(blank=False, null=False)
    completed = models.BooleanField(default=False)
    deadline = models.DateTimeField(
        auto_now_add=False, validators=[validate_deadline], null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.ref_code:
            code = task_ref_code()
            self.ref_code = code
        super().save(*args, **kwargs)

    def __str__(self):
        return 'Task for- %s' % (self.user.first_name)

    def task_completed_url(self):
        return reverse('dashboard:task-completed', kwargs={'pk': self.id})


class Account(models.Model):
    type_choices = (
        ('C', 'Cash'), ('B', 'Bank'), ('M', 'Mobile'), ('D', 'Deposit')
    )
    name = models.CharField(max_length=20, blank=False, null=False)
    account_type = models.CharField(
        max_length=2, choices=type_choices, default='B')
    opening_balance = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    available_balance = models.IntegerField(blank=True, null=True)
    transactions = models.ManyToManyField(
        'Transaction', related_name='transaction', blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.available_balance:
            self.available_balance = self.opening_balance

        
        super().save(*args, **kwargs)


class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    payee = models.ForeignKey(
        'Payee', related_name='payee', on_delete=models.SET_NULL, null=True, blank=True)
    service = models.ForeignKey('Service', related_name='service',
                                 on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    amount = models.PositiveIntegerField(blank=False, null=False)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    ref_number = models.CharField(
        max_length=20, unique=True, blank=False, null=False, editable=False)

    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)

    def __str__(self):
        return '%s-%s' % (self.payee.name, self.amount)

    def save(self, *args, **kwargs):
        if not self.ref_number:
            self.ref_number = ref_code_generator()

        super().save(*args, **kwargs)

    def delete_url(self):
        return reverse('dashboard:delete-transaction', kwargs={"pk": self.id})

    def edit_url(self):
        return reverse('dashboard:edit-transaction', kwargs={'pk': self.id})

class Payee(models.Model):
    name = models.CharField(max_length=20, blank=False, null=False)

    def __str__(self):
        return self.name


class Service(models.Model):
    
    name = models.CharField(max_length=250, blank=False, null=False)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return '%s' % (self.name)

    class Meta:
        verbose_name = 'service'
        verbose_name_plural = 'services'

class Category(models.Model):
    name = models.CharField(max_length=10, blank=False, null=False)

    def __str__(self):
        return self.name



def account_update(sender, instance, created, *args, **kwargs):
    if created:
        account = instance.account
        if instance.category.name == 'Income':
            print('income')
            account.available_balance += instance.amount
        elif instance.category.name == 'Expense':
            account.available_balance -= instance.amount
            print('Expense')
        account.transactions.add(instance)
        account.save()

    else:
        account = instance.account
        if not instance in account.transactions.all():
            if instance.category.name == 'Income':
                account.available_balance += instance.amount
            elif instance.category.name == 'Expense':
                account.available_balance -= instance.amount
            account.transactions.add(instance)
            account.save()

post_save.connect(account_update, sender=Transaction, weak=False)

