from django.contrib import admin
from django.contrib import messages

from .models import Account, Employee, Asset, Category, Payee, Service, Task, Transaction


class AssetAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'purchase_price')
    readonly_fields=('code',)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('ref_number', 'account', 'category', 'amount')
    readonly_fields = ('ref_number',)
    def save_model(self, request, obj, form, change):
        account = obj.account
        if change:
            transaction = Transaction.objects.get(pk=obj.id)
            if 'amount' in form.changed_data:
                if obj.category.name == 'Income':
                    account.available_balance -= transaction.amount
                    account.available_balance += obj.amount
                elif obj.category.name == 'Expense':
                    account.available_balance += transaction.amount
                    account.available_balance -= obj.amount
                account.save()
                messages.info(request, 'Account updated')
        
        super().save_model(request, obj, form, change)

admin.site.register(Asset, AssetAdmin)
admin.site.register(Task)
admin.site.register(Account)
admin.site.register(Payee)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Service)
admin.site.register(Category)
admin.site.register(Employee)
