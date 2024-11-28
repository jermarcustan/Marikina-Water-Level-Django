from django.contrib import admin

from .models import Dreamer, Dream

admin.site.register([Dreamer, Dream])