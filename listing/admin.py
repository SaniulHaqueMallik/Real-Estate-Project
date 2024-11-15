from django.contrib import admin
from .models import Listing
# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'is_published','city', 'address', 'sqft', 'realtor']
    list_display_links = ('id', 'title', 'realtor')
    list_filter = ['realtor', 'list_date','is_published']
    list_editable = ['is_published']
    search_fields = ('title', 'realtor')
    list_per_page = 20

admin.site.register(Listing, ListingAdmin)