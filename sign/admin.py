#coding=utf-8
from django.contrib import admin
from models import Event,Guest

# Register your models here.
#admin.site.register(Event)
#admin.site.register(Guest)

class EventAdmin(admin.ModelAdmin):
    list_display = ['name','status','start_time','id']
    search_fields = ['name']
    list_filter = ['status']
class GuestAdmin(admin.ModelAdmin):
    list_display = ['realname','phone','email','sign','creat_time','event']
    search_fields = ['realname','phone']
    list_filter = ['sign']
admin.site.register(Event,EventAdmin)
admin.site.register(Guest,GuestAdmin)