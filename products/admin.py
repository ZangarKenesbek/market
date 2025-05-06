from django.contrib import admin
from .models import Category, Product, ProductAdmin

# Register your models here.



admin.site.register(Category)
admin.site.register(Product,ProductAdmin)
admin.site.site_header = "Magnum"
admin.site.site_title = "Magnum panel"
admin.site.index_title = "Welcome"