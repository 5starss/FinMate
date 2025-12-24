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

# 1. 카테고리 삭제 (내가 만든 것만 삭제 가능)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def category_detail(request, category_pk):
    category = get_object_or_404(Category, pk=category_pk)
    
    # 공통 카테고리(user=None)는 삭제 불가, 본인 것만 삭제 가능
    if category.user != request.user:
        return Response({"detail": "공통 카테고리 또는 타인의 카테고리는 삭제할 수 없습니다."}, 
                        status=status.HTTP_403_FORBIDDEN)
    
    category.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


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


# 3. 가계부 상세 조회, 수정, 삭제 기능 (기존 삭제 전용 함수를 확장)
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def transaction_detail(request, transaction_pk):
    # (1) 해당 내역이 있는지 확인
    transaction = get_object_or_404(Transaction, pk=transaction_pk)
    
    # (2) 본인 내역인지 권한 확인
    if transaction.user != request.user:
        return Response({"detail": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

    # 상세 조회 (GET)
    if request.method == 'GET':
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)

    # 수정 (PUT) - 가계부 테이블 수정 기능 대응
    elif request.method == 'PUT':
        # partial=True를 주면 제목만 바꾸거나 금액만 바꾸는 '부분 수정'이 가능해집니다.
        serializer = TransactionSerializer(transaction, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    # 삭제 (DELETE)
    elif request.method == 'DELETE':
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)