from django.contrib import admin
from .models import Products, Customers, Suppliers, Sales, Purchase, SaleDetails, PurchaseDetails, Expense, ExpenseDetails

# Register your models here.
admin.site.register(Purchase)
admin.site.register(Sales)
admin.site.register(Customers)
admin.site.register(Suppliers)
admin.site.register(Products)
admin.site.register(SaleDetails)
admin.site.register(PurchaseDetails)
admin.site.register(Expense)
admin.site.register(ExpenseDetails)
