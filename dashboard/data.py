from .models import Transaction
from django.db.models import Count, Avg, Sum


data = Transaction.objects.values('date_created__month', 'category__name').annotate(Sum('amount')).order_by('date_created__month')