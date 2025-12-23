from django.shortcuts import get_object_or_404, get_list_or_404
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
import requests, json
from .models import DepositProducts, DepositOptions, SavingProducts, SavingOptions, DepositSubscription, SavingSubscription
from .serializers import DepositProductsSerializer, DepositOptionsSerializer, SavingProductsSerializer, SavingOptionsSerializer, DepositProductDetailSerializer, SavingProductDetailSerializer, DepositSubscriptionSerializer, SavingSubscriptionSerializer


API_KEY = settings.API_KEY

@api_view(['GET', 'POST'])
def deposit_list(request):
    if request.method == 'POST':
        url = 'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json'
        params = {
            'auth': API_KEY,
            'topFinGrpNo': '020000',
            'pageNo': '1'
        }
        response = requests.get(url, params=params)
        products_data = response.json()['result']['baseList']
        options_data = response.json()['result']['optionList']

        for data in products_data:
            try:
                tester_name = DepositProducts.objects.get(fin_prdt_cd=data['fin_prdt_cd'])
                continue

            except:
                DepositProducts(
                    fin_prdt_cd = data['fin_prdt_cd'],
                    dcls_month = data['dcls_month'],
                    kor_co_nm = data['kor_co_nm'],
                    fin_prdt_nm = data['fin_prdt_nm'],
                    etc_note = data['etc_note'],
                    join_deny = data['join_deny'],
                    join_member = data['join_member'],
                    join_way = data['join_way'],
                    spcl_cnd = data['spcl_cnd'],
                ).save()

        DepositOptions.objects.all().delete()
        for data in options_data:
            fin_prdt_cd = data['fin_prdt_cd']
            product_obj = DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
            DepositOptions(
                intr_rate_type_nm = data['intr_rate_type_nm'],
                intr_rate = data['intr_rate'],
                intr_rate2 = data['intr_rate2'],
                save_trm = data['save_trm'],
                fin_prdt_cd = product_obj,
            ).save()

        return Response(
            {"message": "Okay"},
            status=status.HTTP_200_OK
        )
    elif request.method == 'GET':
        deposit = get_list_or_404(DepositProducts)
        serializer = DepositProductsSerializer(deposit, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def saving_list(request):
    if request.method == 'POST':
        url = 'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json'
        params = {
            'auth': API_KEY,
            'topFinGrpNo': '020000',
            'pageNo': '1'
        }
        response = requests.get(url, params=params)
        products_data = response.json()['result']['baseList']
        options_data = response.json()['result']['optionList']

        for data in products_data:
            try:
                tester_name = SavingProducts.objects.get(fin_prdt_cd=data['fin_prdt_cd'])
                continue

            except:
                SavingProducts(
                    fin_prdt_cd = data['fin_prdt_cd'],
                    dcls_month = data['dcls_month'],
                    kor_co_nm = data['kor_co_nm'],
                    fin_prdt_nm = data['fin_prdt_nm'],
                    etc_note = data['etc_note'],
                    join_deny = data['join_deny'],
                    join_member = data['join_member'],
                    join_way = data['join_way'],
                    spcl_cnd = data['spcl_cnd'],
                ).save()

        SavingOptions.objects.all().delete()
        for data in options_data:
            fin_prdt_cd = data['fin_prdt_cd']
            product_obj = SavingProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
            SavingOptions(
                intr_rate_type_nm = data['intr_rate_type_nm'],
                intr_rate = data['intr_rate'],
                intr_rate2 = data['intr_rate2'],
                save_trm = data['save_trm'],
                fin_prdt_cd = product_obj,
            ).save()

        return Response(
            {"message": "Okay"},
            status=status.HTTP_200_OK
        )
    elif request.method == 'GET':
        saving = get_list_or_404(SavingProducts)
        serializer = SavingProductsSerializer(saving, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def deposit_detail(request, pk):
    product = get_object_or_404(DepositProducts, pk=pk)
    data = DepositProductDetailSerializer(product).data

    # Vue 편의: 로그인 유저면 가입 여부도 같이 내려줌
    data["is_joined"] = (
        request.user.is_authenticated and
        DepositSubscription.objects.filter(user=request.user, product=product).exists()
    )
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
def saving_detail(request, pk):
    product = get_object_or_404(SavingProducts, pk=pk)
    data = SavingProductDetailSerializer(product).data
    data["is_joined"] = (
        request.user.is_authenticated and
        SavingSubscription.objects.filter(user=request.user, product=product).exists()
    )
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def deposit_subscribe(request, product_id):
    product = get_object_or_404(DepositProducts, pk=product_id)

    # 1. 가입하기 (POST)
    if request.method == 'POST':
        if DepositSubscription.objects.filter(user=request.user, deposit_product=product).exists():
            return Response({"message": "이미 가입한 예금 상품입니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        DepositSubscription.objects.create(user=request.user, deposit_product=product)
        return Response({"message": "예금 상품 가입 완료"}, status=status.HTTP_201_CREATED)

    # 2. 특정 유저의 가입 여부 확인 등 (GET - 필요시)
    elif request.method == 'GET':
        subscription = DepositSubscription.objects.filter(user=request.user, deposit_product=product).first()
        serializer = DepositSubscriptionSerializer(subscription)
        return Response(serializer.data)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def saving_subscribe(request, product_id):
    product = get_object_or_404(SavingProducts, pk=product_id)

    if request.method == 'POST':
        if SavingSubscription.objects.filter(user=request.user, saving_product=product).exists():
            return Response({"message": "이미 가입한 적금 상품입니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        SavingSubscription.objects.create(user=request.user, saving_product=product)
        return Response({"message": "적금 상품 가입 완료"}, status=status.HTTP_201_CREATED)

    elif request.method == 'GET':
        subscription = SavingSubscription.objects.filter(user=request.user, saving_product=product).first()
        serializer = SavingSubscriptionSerializer(subscription)
        return Response(serializer.data)

# [추가] 유저 페이지에서 전체 가입 목록을 가져올 때 사용할 뷰
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_all_subscriptions(request):
    deposit_subs = DepositSubscription.objects.filter(user=request.user)
    saving_subs = SavingSubscription.objects.filter(user=request.user)
    
    d_serializer = DepositSubscriptionSerializer(deposit_subs, many=True)
    s_serializer = SavingSubscriptionSerializer(saving_subs, many=True)
    
    return Response({
        "deposits": d_serializer.data,
        "savings": s_serializer.data
    })
    