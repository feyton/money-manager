from django.contrib import admin

from .models import Account, Employee, Asset, Category, Payee, Service, Task, Transaction


class AssetAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'purchase_price')
    readonly_fields=('code',)

admin.site.register(Asset, AssetAdmin)
admin.site.register(Task)
admin.site.register(Account)
admin.site.register(Payee)
admin.site.register(Transaction)
admin.site.register(Service)
admin.site.register(Category)
admin.site.register(Employee)
