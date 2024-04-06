from django.urls import path
from . import views


urlpatterns = [
    path('', views.finance, name='finance'),
    path('transactions/', views.TransactionListView.as_view(), name='transaction_list'),
    path('transactions/<int:transaction_id>', views.transaction_detail, name='transaction_detail'),
    path('transactions/new/', views.transaction_form, name='transaction_form'),
]