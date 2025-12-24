from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404, get_list_or_404
from .models import Article, Comment
from .serializers import ArticleListSerializer, ArticleSerializer, CommentSerializer
from django.db.models import Sum

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def article_list_create(request):
    # 1. 목록 조회
    if request.method == 'GET':
        articles = Article.objects.all().order_by('-created_at')
        # 만약 특정 상품 상세페이지에서 접근했다면 필터링
        product_code = request.query_params.get('product_code')
        if product_code:
            articles = articles.filter(product_code=product_code)
            
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)

    # 2. 게시글 생성
    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        
        # [수정] validate_ok()를 is_valid(raise_exception=True)로 변경
        if serializer.is_valid(raise_exception=True):
            # --- 자산 및 소비패턴 스냅샷 로직 ---
            user = request.user
            
            # (1) 총 자산 계산
            income = user.transactions.filter(category__type='INCOME').aggregate(Sum('amount'))['amount__sum'] or 0
            expense = user.transactions.filter(category__type='EXPENSE').aggregate(Sum('amount'))['amount__sum'] or 0
            current_cash = income - expense
            
            # (2) 주 소비 카테고리 추출
            top_category = user.transactions.filter(category__type='EXPENSE') \
                            .values('category__name') \
                            .annotate(total=Sum('amount')) \
                            .order_by('-total').first()
            
            rep_cat = top_category['category__name'] if top_category else "미설정"
            
            # 데이터 저장
            serializer.save(
                user=user, 
                total_asset_snapshot=current_cash, 
                representative_category=rep_cat
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated]) # 기본적으로 로그인한 사용자만 접근 가능
def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    # 1. 상세 조회는 누구나(로그인 유저라면) 가능
    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    # 2. 수정 및 삭제는 반드시 작성자 본인이어야 함
    elif request.method in ['PUT', 'DELETE']:
        if request.user != article.user:
            return Response(
                {'error': '권한이 없습니다. 작성자만 수정/삭제할 수 있습니다.'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        if request.method == 'PUT':
            serializer = ArticleSerializer(article, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        
        elif request.method == 'DELETE':
            article.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def article_like(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if article.like_users.filter(pk=request.user.pk).exists():
        article.like_users.remove(request.user)
    else:
        article.like_users.add(request.user)
    return Response(status=status.HTTP_200_OK)

# 댓글 기능 추가
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_create(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user, article=article)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def comment_delete(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_403_FORBIDDEN)