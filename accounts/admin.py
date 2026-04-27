from django.contrib import admin
from .models import User, CandidateProfile, RecruiterProfile

admin.site.register(User)
admin.site.register(CandidateProfile)
admin.site.register(RecruiterProfile)