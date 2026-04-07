from django.contrib import admin
from .models import BookingEnquiry

@admin.register(BookingEnquiry)
class BookingEnquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'package', 'destination', 'travel_date', 'travelers', 'status', 'created_at']
    list_filter = ['status', 'travel_date', 'created_at']
    search_fields = ['name', 'email', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Booking Details', {
            'fields': ('package', 'destination', 'travel_date', 'travelers')
        }),
        ('Additional Information', {
            'fields': ('special_requests',)
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )