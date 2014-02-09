from django.contrib import admin

# Register your models here.
from linecook.models import Recipe, Step, User, Appliance, Food, UserAppliance

admin.site.register(Recipe)
admin.site.register(Step)
admin.site.register(User)
admin.site.register(Appliance)
admin.site.register(UserAppliance)
admin.site.register(Food)
