from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.category_list),      # 카테고리 목록 (선택박스용)
    path('transactions/', views.transaction_list_create), # 내역 조회 및 생성
]