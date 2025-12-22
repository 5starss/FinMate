from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings 

# 1. 커스텀 유저 모델 정의
class User(AbstractUser):
    pass

# 2. 프로필 모델 정의
class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    # get_user_model() 대신 settings.AUTH_USER_MODEL 사용
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='profile'
    )
    age = models.IntegerField(null=True, blank=True)
    income = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True) #성별 데이터
    spending_habits = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.user.username