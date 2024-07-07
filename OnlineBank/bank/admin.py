from django.contrib import admin
from .models import User, Deposit_History, Debit_History, Credit_History, Notification
# Register your models here.




admin.site.register(User)
admin.site.register(Deposit_History)
admin.site.register(Credit_History)
admin.site.register(Debit_History)
admin.site.register(Notification)