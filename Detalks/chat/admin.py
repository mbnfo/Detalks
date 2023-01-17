from django.contrib import admin
from .models import Room, Message,Profile,Option,Catagories,Saver

# Register your models here.
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Profile)
admin.site.register(Option)
admin.site.register(Catagories)
admin.site.register(Saver)

