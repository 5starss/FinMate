from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings 
import datetime

# 1. 커스텀 유저 모델 정의
class User(AbstractUser):
    # nickname을 CharField로 정의하고 공백을 허용합니다.
    nickname = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.username

# 2. 프로필 모델 정의
class UserProfile(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female')]
    
    # related_name='profile' 설정은 UserSerializer에서 역참조할 때 필수입니다.
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='profile'
    )
    
    # 생년월일 및 자산 정보
    birth_date = models.DateField(null=True, blank=True) 
    income = models.BigIntegerField(default=0, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    spending_habits = models.CharField(max_length=255, null=True, blank=True)
    
    # 이미지 필드: upload_to는 media/profile/ 경로에 저장하게 합니다.
    # blank=True는 폼 전송 시 비어있어도 됨을 의미하고, null=True는 DB에 빈 값 저장을 허용합니다.
    image = models.ImageField(upload_to='profile/', null=True, blank=True)

    # 현재 날짜 기준으로 나이를 계산하는 프로퍼티
    @property
    def age(self):
        if self.birth_date:
            today = datetime.date.today()
            # 생일이 지났는지 여부를 체크하여 정확한 만 나이 계산
            return today.year - self.birth_date.year - (
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
            )
        return None

    def __str__(self):
        return f"{self.user.username}'s profile"