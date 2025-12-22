from django.urls import path
from . import views

urlpatterns = [
    # 이제 /accounts/profile/ 주소로 요청을 보내면 위 함수가 실행됩니다.
    path('profile/', views.user_profile_detail),
]