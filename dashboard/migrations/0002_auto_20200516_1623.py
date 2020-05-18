# Generated by Django 3.0.2 on 2020-05-16 14:23

import dashboard.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='purchase_date',
            field=models.DateField(blank=True, null=True, validators=[dashboard.models.validate_purchase_date]),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('ref_code', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
                ('action', models.TextField()),
                ('completed', models.BooleanField(default=False)),
                ('deadline', models.DateTimeField(validators=[dashboard.models.validate_deadline])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
