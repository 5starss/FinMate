from django.db import models
from django.conf import settings

class Category(models.Model):
    INCOME_EXPENSE_CHOICES = [('INCOME', '수입'), ('EXPENSE', '지출')]
    
    # name에 null=False(기본값)와 빈 문자열 방지 로직
    name = models.CharField(max_length=20) 
    type = models.CharField(max_length=10, choices=INCOME_EXPENSE_CHOICES)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )

    class Meta:
        # ✅ 동일 유저 내에서 같은 이름+타입의 카테고리 중복 생성 방지
        # user가 null인 공통 카테고리들 사이에서도 중복 방지
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'type'], 
                name='unique_user_category'
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.type})"

class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions')
    # 카테고리가 삭제되어도 내역은 남도록 SET_NULL 유지 (좋은 선택입니다!)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='transactions')
    title = models.CharField(max_length=100)
    amount = models.IntegerField()
    date = models.DateField()
    memo = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.date} | {self.title} | {self.amount}"

class Budget(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='budgets')
    month = models.DateField() 
    planned_amount = models.IntegerField()

    class Meta:
    # 한 유저가 같은 달(1일 기준)에 예산을 중복 생성하는 것 방지
        unique_together = ['user', 'month']

    def __str__(self):
        return f"{self.user.username} - {self.month.strftime('%Y-%m')} 예산"