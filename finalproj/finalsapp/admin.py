from django.contrib import admin
from .models import DateTime, Record

# Register your models here.
admin.site.register([DateTime, Record])