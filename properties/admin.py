from django.contrib import admin
from .models import InvitationCode

@admin.register(InvitationCode)
class InvitationCodeAdmin(admin.ModelAdmin):
    list_display    = ('code', 'created_at', 'used', 'property')
    list_filter     = ('used',)
    readonly_fields = ('code', 'created_at')
