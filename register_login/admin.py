from django.contrib import admin
from .models import Users, Inbox, Deleted, Sent
# Register your models here.

admin.site.register(Users)
admin.site.register(Inbox)
admin.site.register(Deleted)
admin.site.register(Sent)