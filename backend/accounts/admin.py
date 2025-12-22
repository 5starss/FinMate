from django.contrib import admin
from .models import UserProfile

admin.site.register(UserProfile)  # UserProfile 모델을 Admin에 등록
