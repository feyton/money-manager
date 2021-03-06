# Generated by Django 3.0.2 on 2020-05-17 08:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_auto_20200516_1623'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('account_type', models.CharField(choices=[('C', 'Cah'), ('B', 'Bank'), ('M', 'Mobile'), ('D', 'Deposit')], default='B', max_length=2)),
                ('opening_balance', models.PositiveIntegerField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Payee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='TransactionCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('category_type', models.CharField(choices=[('I', 'Income'), ('E', 'Expense')], default='I', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('amount', models.PositiveIntegerField()),
                ('ref_number', models.CharField(editable=False, max_length=20, unique=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Account')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category', to='dashboard.TransactionCategory')),
                ('payee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payee', to='dashboard.Payee')),
            ],
        ),
    ]
