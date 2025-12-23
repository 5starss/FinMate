from django.urls import path
from . import views

urlpatterns = [
    # 1. 전체 상품 리스트 및 API 데이터 저장
    path('deposit-list/', views.deposit_list, name='deposit_list'),
    path('saving-list/', views.saving_list, name='saving_list'),

    # 2. 개별 상품 상세 조회 (views.py 인자: pk)
    path('deposits/<int:pk>/', views.deposit_detail, name='deposit_detail'),
    path('savings/<int:pk>/', views.saving_detail, name='saving_detail'),

    # 3. 상품 가입하기 및 확인 (views.py 인자: product_id)
    path('deposits/<int:product_id>/subscribe/', views.deposit_subscribe, name='deposit_subscribe'),
    path('savings/<int:product_id>/subscribe/', views.saving_subscribe, name='saving_subscribe'),

    # 4. 상품 가입해지 
    path('deposits/unsubscribe/<int:subscription_id>/', views.deposit_unsubscribe),
    path('savings/unsubscribe/<int:subscription_id>/', views.saving_unsubscribe),
    
    # 5. 유저 페이지용 전체 가입 목록
    path('user-subscriptions/', views.user_all_subscriptions, name='user_all_subscriptions'),
]