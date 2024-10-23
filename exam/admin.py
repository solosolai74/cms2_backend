from django.contrib import admin

# Register your models here.
from .models  import *
# Register your models here.
from django.apps import apps
from django.contrib import admin


class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']

class EncKeyStoreAdmin(admin.ModelAdmin):
    list_display = ("examslot", "papertype", "toprocess", "record_created_at")
    ordering = ("examslot",)

class UserVisitAdmin(admin.ModelAdmin):

    list_display = ("session_start", "user", "session_key", "last_accessed", "session_end", "remote_addr")
    list_filter = ("session_start",)
    search_fields = (
        "user__first_name",
        "user__last_name",
        "user__username",
        "ua_string",
    )
    raw_id_fields = ("user",)
    readonly_fields = (
        "user",
        "hash",
        "session_start",
        "last_accessed",
        "session_end",
        "session_key",
        "remote_addr",
        # "user_agent",
        "ua_string",
        "created_at",
    )
    ordering = ("-session_start",)


admin.site.register(UserVisit, UserVisitAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(EncKeyStore, EncKeyStoreAdmin)

models = apps.get_models()

for model in models:
    try:
        admin.site.register(model)
    except:
        pass

