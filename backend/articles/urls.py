from django.urls import path
from . import views

app_name = 'articles'
urlpatterns = [
    # 게시글 전체 목록 조회 및 생성
    path('', views.article_list_create, name='article_list_create'),
    
    # 게시글 상세 조회, 수정, 삭제
    path('<int:article_pk>/', views.article_detail, name='article_detail'),
    
    # 게시글 좋아요
    path('<int:article_pk>/like/', views.article_like, name='article_like'),
    
    # 댓글 생성 (조회는 게시글 상세에 포함되어 있음)
    path('<int:article_pk>/comments/', views.comment_create, name='comment_create'),
    
    # 댓글 삭제
    path('comments/<int:comment_pk>/', views.comment_delete, name='comment_delete'),
]