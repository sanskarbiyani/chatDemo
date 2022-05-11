from django.contrib import admin
from chat.models import Thread, Messages

# Register your models here.
admin.site.register(Thread)
admin.site.register(Messages)
