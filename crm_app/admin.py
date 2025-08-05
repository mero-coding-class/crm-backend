from django.contrib import admin
from . models import User, Course, Lead, Enrollment, LeadLog

admin.site.register(Course)
admin.site.register(Lead)
admin.site.register(Enrollment)
admin.site.register(User)
admin.site.register(LeadLog)