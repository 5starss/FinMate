from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.category_list_create), # ✅ 바뀐 이름으로 수정
    path('transactions/', views.transaction_list_create), # 내역 조회 및 생성
    path('transactions/<int:transaction_pk>/', views.transaction_detail), # 삭제
]