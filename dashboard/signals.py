from django.db.models.signals import post_save, pre_save, pre_delete
from dashboard.models import Account, Transaction, Service
from django.dispatch import Signal, receiver


# def transaction_receiver(sender, instance, created, *args, **kwargs):
#     if created:
#         account = instance.account
#         category = instance.category.category_type
#         if category == 'I':
#             acc = Account.objects.get(id=account.id)
#             acc.available_balance = (acc.available_balance + instance.amount)
#             acc.save()
#         elif category == 'E':
#             acc = Account.objects.get(id=account.id)
#             acc.available_balance = (acc.available_balance - instance.amount)
#             acc.save()
#         else:
#             print('Error while sending signale')


# post_save.connect(transaction_receiver, sender=Transaction)

@receiver(post_save, sender=Transaction)
def account_update(sender, instance, created, *args, **kwargs):
    if created:
        account = instance.account
        account.transactions.add(instance)
        account.save()


