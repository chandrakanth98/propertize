from django.contrib import admin
from .models import Property, InvitationCode, ProxyTenant, PropertyNotice

# Register your models here.

admin.site.register(Property)
admin.site.register(InvitationCode)
admin.site.register(ProxyTenant)
admin.site.register(PropertyNotice)

