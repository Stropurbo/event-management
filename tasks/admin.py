from django.contrib import admin
from tasks.models import Event,Category,Speaker

# Register your models here.
admin.site.register(Event)
admin.site.register(Category)
admin.site.register(Speaker)

# admin.site.register(Participant)