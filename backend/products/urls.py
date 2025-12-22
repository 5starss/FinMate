from django.urls import path
from . import views

urlpatterns = [
    path('deposit/', views.deposit_list),  # 리스트 조회 기능 유지
    path('saving/', views.saving_list),  # 리스트 조회 기능 유지

    # 상세 조회 및 구독 관련 API 경로 수정
    path('deposits/<int:pk>/', views.deposit_detail, name='deposit_detail'),
    path('deposits/<int:pk>/subscribe/', views.deposit_subscribe, name='deposit_subscribe'),
    
    path('savings/<int:pk>/', views.saving_detail, name='saving_detail'),
    path('savings/<int:pk>/subscribe/', views.saving_subscribe, name='saving_subscribe'),
]
