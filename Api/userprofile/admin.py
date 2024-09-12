from django.contrib import admin
from  .models import profile, bodyProfile, personal_calendar, subPersonalCalendar, subscribeHashtag
# Register your models here.


admin.site.register(profile)
admin.site.register(bodyProfile)
admin.site.register(personal_calendar)
admin.site.register(subPersonalCalendar)
admin.site.register(subscribeHashtag)