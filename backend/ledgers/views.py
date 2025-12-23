from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Transaction, Category
from .serializers import TransactionSerializer, CategorySerializer

# 1. 카테고리 목록 조회 (입력 폼에서 선택하기 위함)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def category_list(request):
    categories = Category.objects.all()
    serailizer = CategorySerializer(categories, many=True)
    return Response(serailizer.data)

# 2. 내역 생성 및 전체 목록 조회
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def transaction_list_create(request):
    # GET: 현재 유저의 전체 내역 조회
    if request.method == 'GET':
        transactions = Transaction.objects.filter(user=request.user).order_by('-date', '-created_at')
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
    
    # POST: 새로운 내역 기록
    elif request.method == 'POST':
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # 현재 로그인한 유저를 자동으로 할당하여 저장
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)