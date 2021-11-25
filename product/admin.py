from django.contrib import admin
from . import models


class VariationInline(admin.TabularInline):
    model = models.Variation
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'short_description',
                    'get_price_format', 'get_promotional_price_format']
    inlines = [VariationInline]


admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Variation)
