from django.db import models
from django.conf import settings

class Category(models.Model):
    # 식비, 교통비, 월급, 부수입 등
    # 수입용 카테고리와 지출용 카테고리를 구분합니다.
    INCOME_EXPENSE_CHOICES = [('INCOME', '수입'), ('EXPENSE', '지출')]
    
    name = models.CharField(max_length=20)
    type = models.CharField(max_length=10, choices=INCOME_EXPENSE_CHOICES)

    def __str__(self):
        return f"[{self.type}] {self.name}"

class Transaction(models.Model):
    # 실제 수입/지출 내역
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100) # 내역명 (예: 점심식사)
    amount = models.IntegerField() # 금액
    date = models.DateField() # 거래 날짜
    memo = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.date} | {self.title} | {self.amount}"

class Budget(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # 2025-12-01 형식으로 저장하되 '그 달의 예산'임을 약속
    month = models.DateField() 
    planned_amount = models.IntegerField()

    class Meta:
        # 한 유저가 같은 달(1일 기준)에 예산을 중복 생성하는 것 방지
        unique_together = ['user', 'month']

    def __str__(self):
        return f"{self.user.username} - {self.month.strftime('%Y-%m')} 예산"