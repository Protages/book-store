from django.contrib import admin
from .models import User, ConnectionHistory


admin.site.register(User)
admin.site.register(ConnectionHistory)
