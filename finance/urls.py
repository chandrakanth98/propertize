from django.urls import path
from . import views


urlpatterns = [
    path('', views.finance, name='finance'),
    path('transactions/', views.TransactionListView.as_view(), name='transaction_list'),
]