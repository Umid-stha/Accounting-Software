from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login', views.loginUser , name='login'),

    path('sales/', views.sales, name='sales'),
    path('purchase/', views.purchase, name='purchase'),
    path('expense/', views.expenses, name='expense'),
    path('reports/', views.report, name='reports'),
    path('Products/', views.product, name='product'),
    path('Customer/', views.Customer, name='Customer'),

    path('SalesReport/', views.salesReport, name='sales-report'),
    path('viewSales/<str:pk>/', views.viewSales, name='viewSales'),
    path('deleteSales/<str:pk>/', views.deleteSales, name='deleteSales'),

    path('PurchaseReport/', views.purchaseReport, name='purchase-report'),
    path('viewPurchase/<str:pk>/', views.viewPurchase, name='viewPurchase'),
    path('deletePurchase/<str:pk>/', views.deletePurchase, name='deletePurchase'),

    path('expenseReport/', views.expenseReport, name='expenseReport'),
    path('viewExpense/<str:pk>/', views.viewExpense, name='viewExpense'),
    path('deleteExpense/<str:pk>/', views.deleteExpense, name='deleteExpense'),

    path('stockReport/', views.stockReport, name='stock-report'),

    path('customerReport/', views.customerReport, name='customer-report'),
    path('viewCustomer/<str:pk>/', views.viewCustomer, name='viewCustomer'),

    path('supplierReport/', views.supplierReport, name='supplier-report'),
    path('viewSupplier/<str:pk>/', views.viewSupplier, name='viewSupplier'),

    path('get-product-details/', views.get_product_details, name='get_product_details'),
    path('get-customer-details/', views.get_customer_details, name='get_customer_details'),
    path('get-supplier-details/', views.get_supplier_details, name='get_supplier_details'),
]