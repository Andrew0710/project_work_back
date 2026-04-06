from django.contrib import admin
from .models import SubscriptionPlan, StudentSubscription

admin.site.register(SubscriptionPlan)
admin.site.register(StudentSubscription)
