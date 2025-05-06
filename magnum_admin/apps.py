
from django.contrib.admin.apps import AdminConfig
class MagnumAdminConfig(AdminConfig):
    default_site = 'magnum_admin.admin.MagnumAdmin'