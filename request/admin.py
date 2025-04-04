from django.contrib import admin
from .models import Request, Comment,ClientRequest

admin.site.register(Request)
admin.site.register(Comment)
admin.site.register(ClientRequest)

# Register your models here.
