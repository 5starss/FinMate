from django.conf import settings  
from django.db import models

class Article(models.Model):
    # 1. 기본 정보
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=100)
    content = models.TextField()
    
    # 2. 데이터 기반 필드 (분석 및 랭킹용)
    # 포트폴리오 공유 시 당시의 자산/수익률 등을 스냅샷 형태로 저장하거나 링크
    total_asset_snapshot = models.BigIntegerField(default=0, help_text="공유 시점의 총 자산")
    representative_category = models.CharField(max_length=20, null=True, blank=True, help_text="가장 많이 소비하는 카테고리 (매칭용)")
    
    # 3. 상품 연동 필드 (특정 상품 상세페이지와 연결용)
    # 상품 ID를 저장하여 특정 예적금 커뮤니티 글만 필터링 가능하게 함
    product_code = models.CharField(max_length=50, null=True, blank=True, help_text="연관된 금융상품 코드")
    product_name = models.CharField(max_length=100, null=True, blank=True)

    # 4. 소셜 기능
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_articles')
    
    # 5. 시간 정보
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)