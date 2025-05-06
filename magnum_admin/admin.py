
from django.contrib import admin

class MagnumAdmin(admin.AdminSite):
    site_header = "Magnum Administration"
    logout_template = "admin/logout.html"
