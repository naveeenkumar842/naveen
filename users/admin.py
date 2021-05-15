from django.contrib import admin
from users.models import Profile

# Register your models here.
class profileAdmin(admin.ModelAdmin):
    list_display = ['user', 'image']

admin.site.register(Profile,profileAdmin)
