from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.category_list_create),
    path('categories/<int:category_pk>/', views.category_detail), # 카테고리 삭제용 추가
    path('transactions/', views.transaction_list_create),
    path('transactions/<int:transaction_pk>/', views.transaction_detail), # GET/PUT/DELETE 통합
]