from django.db import models
from django.conf import settings

# Create your models here.
class DepositProducts(models.Model):
    fin_prdt_cd = models.CharField(max_length=50)
    dcls_month = models.CharField(max_length=6)
    kor_co_nm = models.CharField(max_length=50)
    fin_prdt_nm = models.CharField(max_length=50)
    etc_note = models.TextField()
    join_deny = models.IntegerField()
    join_member = models.CharField(max_length=50)
    join_way = models.CharField(max_length=50)
    spcl_cnd = models.TextField()

    def __str__(self):
        return f"{self.kor_co_nm} - {self.fin_prdt_nm}"
    
class DepositOptions(models.Model):
    intr_rate_type_nm = models.CharField(max_length=50)
    intr_rate = models.FloatField(default=-1)
    intr_rate2 = models.FloatField(default=-1)
    save_trm = models.FloatField()
    fin_prdt_cd = models.ForeignKey(DepositProducts, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.intr_rate_type_nm} - {self.save_trm}개월 ({self.intr_rate_type_nm})"


class SavingProducts(models.Model):
    fin_prdt_cd = models.CharField(max_length=50)
    dcls_month = models.CharField(max_length=6)
    kor_co_nm = models.CharField(max_length=50)
    fin_prdt_nm = models.CharField(max_length=50)
    etc_note = models.TextField()
    join_deny = models.IntegerField()
    join_member = models.CharField(max_length=50)
    join_way = models.CharField(max_length=50)
    spcl_cnd = models.TextField()

    def __str__(self):
        return f"{self.kor_co_nm} - {self.fin_prdt_nm}"
    
class SavingOptions(models.Model):
    intr_rate_type_nm = models.CharField(max_length=50)
    intr_rate = models.FloatField(default=-1)
    intr_rate2 = models.FloatField(default=-1)
    save_trm = models.FloatField()
    fin_prdt_cd = models.ForeignKey(SavingProducts, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.intr_rate_type_nm} - {self.save_trm}개월 ({self.intr_rate_type_nm})"

class DepositSubscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(DepositProducts, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "product"], name="uniq_user_deposit_product")
        ]

class SavingSubscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(SavingProducts, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "product"], name="uniq_user_saving_product")
        ]
