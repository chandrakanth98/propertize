import django_tables2 as tables
from .models import Transaction

class TransactionTable(tables.Table):
    full_name = tables.Column(verbose_name='Full Name', accessor='user', order_by=('user__first_name', 'user__last_name'))

    class Meta:
        model = Transaction
        orderable = True
        attrs = {
            "class": "table table-hover",
            'thead': {"class": ""}
            }
        fields = ("transaction_id", "status", "due_date", "amount", "full_name", "type",)

    def render_full_name(self, record):
        return f"{record.user.first_name} {record.user.last_name}"