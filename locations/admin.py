from django.contrib import admin
from .models import Country, State, City


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'shortname', 'phonecode')
    search_fields = ('name', 'shortname')
    ordering = ('name',)


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country')
    list_filter = ('country',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'state', 'get_country')
    list_filter = ('state', 'state__country')
    search_fields = ('name',)
    ordering = ('name',)
    
    def get_country(self, obj):
        return obj.state.country.name
    get_country.short_description = 'Country'
    get_country.admin_order_field = 'state__country__name'