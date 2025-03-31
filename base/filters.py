import django_filters
from django_filters import DateFilter, DateFromToRangeFilter
from .models import *

class saleFilter(django_filters.FilterSet):
    date_range = DateFromToRangeFilter(field_name="sale_date", widget=django_filters.widgets.RangeWidget(attrs={'type': 'date'}))
    class Meta:
        model=Sales
        fields = '__all__'
        exclude = ['updated','created', 'sale_date']

class purchaseFilter(django_filters.FilterSet):
    date_range = DateFromToRangeFilter(field_name="pur_date", widget=django_filters.widgets.RangeWidget(attrs={'type': 'date'}))
    class Meta:
        model=Purchase
        fields = '__all__'
        exclude = ['updated','created', 'pur_date']

class productFilter(django_filters.FilterSet):
    class Meta:
        model=Products
        fields = '__all__'

class customerFilter(django_filters.FilterSet):
    class Meta:
        model=Customers
        fields = '__all__'
        exclude = ['created']

class supplierFilter(django_filters.FilterSet):
    class Meta:
        model=Suppliers
        fields = '__all__'
        exclude = ['created']

class expenseFilter(django_filters.FilterSet):
    date_range = DateFromToRangeFilter(field_name="created", widget=django_filters.widgets.RangeWidget(attrs={'type': 'date'}))
    class Meta:
        model=Expense
        fields = '__all__'
        exclude = ['created']