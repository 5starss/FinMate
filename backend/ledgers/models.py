from django.db import models
from django.conf import settings

class Category(models.Model):
    INCOME_EXPENSE_CHOICES = [('INCOME', '수입'), ('EXPENSE', '지출')]
    
    name = models.CharField(max_length=20)
    type = models.CharField(max_length=10, choices=INCOME_EXPENSE_CHOICES)
    
    # ✅ 추가된 부분: 운영자용(null)과 유저용을 구분합니다.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='categories'
    )

    def __str__(self):
        # 관리자 페이지에서 구분이 쉽도록 표시
        owner = "공통" if not self.user else self.user.username
        return f"[{owner}] [{self.type}] {self.name}"

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