from django.contrib import admin
from MedBotApp.models import MyUser, ChatRecords, ImageRecords, GuestChatRecords

# Register your models here.
admin.site.register(MyUser)
admin.site.register(ChatRecords)
admin.site.register(GuestChatRecords)
admin.site.register(ImageRecords)
