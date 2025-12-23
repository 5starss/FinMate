from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q  # 복합 쿼리를 위해 추가
from .models import Transaction, Category
from .serializers import TransactionSerializer, CategorySerializer

# 1. 카테고리 목록 조회 및 생성 (사용자가 직접 입력한 카테고리 등록 포함)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def category_list_create(request):
    # GET: 카테고리 목록 불러오기
    if request.method == 'GET':
        # (1) 공통 카테고리(user=None)와 (2) 현재 유저의 카테고리만 가져옴
        categories = Category.objects.filter(
            Q(user__isnull=True) | Q(user=request.user)
        )
        
        # [차트/폼용] 수입 또는 지출 타입 필터링 (?type=INCOME)
        category_type = request.query_params.get('type')
        if category_type:
            categories = categories.filter(type=category_type)
            
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    # POST: 새로운 개인 카테고리 등록 (사용자가 텍스트 직접 입력 시)
    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # 현재 로그인한 유저를 주인으로 설정하여 저장
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# 2. 내역 생성 및 전체 목록 조회 (차트 필터링 기능 추가)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def transaction_list_create(request):
    if request.method == 'GET':
        # 현재 유저의 전체 내역 조회
        transactions = Transaction.objects.filter(user=request.user).order_by('-date', '-created_at')
        
        # [차트 시각화용] 수입/지출 버튼 클릭 시 필터링 (?type=EXPENSE)
        transaction_type = request.query_params.get('type')
        if transaction_type:
            # 카테고리의 타입을 기준으로 필터링
            transactions = transactions.filter(category__type=transaction_type)
            
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# 3. 가계부 삭제 기능 (유지)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def transaction_detail(request, transaction_pk):
    transaction = get_object_or_404(Transaction, pk=transaction_pk)
    
    if request.user == transaction.user:
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_403_FORBIDDEN)