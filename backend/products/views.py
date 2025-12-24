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
        serializer = DepositProductDetailSerializer(deposit, many=True)
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
        serializer = SavingProductDetailSerializer(saving, many=True)
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
        # 프론트엔드에서 보낸 option_id 가져오기
        option_id = request.data.get('option_id')
        amount = request.data.get('amount') # 👈 여기가 None이면 에러 발생

        # 데이터 검증 (에러 방지용 가드)
        if amount is None or amount == "":
            return Response({"message": "가입 금액(amount)이 누락되었습니다."}, status=400)
        
        if not option_id:
            return Response({"message": "기간(옵션)을 선택해주세요."}, status=status.HTTP_400_BAD_REQUEST)

        # 1-1. 이미 해당 '상품'에 가입했는지 확인 (UniqueConstraint 기준)
        if DepositSubscription.objects.filter(user=request.user, product=product).exists():
            return Response({"message": "이미 가입한 예금 상품입니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        # 1-2. 선택한 옵션 객체 가져오기
        option = get_object_or_404(DepositOptions, pk=option_id)

        # 1-3. 가입 정보 저장 (선택한 옵션 포함)
        DepositSubscription.objects.create(
            user=request.user, 
            product=product,
            deposit_option=option,  # 모델에 추가한 필드명과 일치해야 합니다
            amount=int(amount) # ✅ 가입 금액 저장
        )
        return Response({"message": "예금 상품 가입 완료"}, status=status.HTTP_201_CREATED)

    # 2. 특정 유저의 가입 여부 확인 (GET)
    elif request.method == 'GET':
        subscription = DepositSubscription.objects.filter(user=request.user, product=product).first()
        serializer = DepositSubscriptionSerializer(subscription)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def saving_subscribe(request, product_id):
    product = get_object_or_404(SavingProducts, pk=product_id)

    if request.method == 'POST':
        option_id = request.data.get('option_id')
        amount = request.data.get('amount') # 👈 여기가 None이면 에러 발생

        # 데이터 검증 (에러 방지용 가드)
        if amount is None or amount == "":
            return Response({"message": "가입 금액(amount)이 누락되었습니다."}, status=400)
        if not option_id:
            return Response({"message": "기간(옵션)을 선택해주세요."}, status=status.HTTP_400_BAD_REQUEST)

        if SavingSubscription.objects.filter(user=request.user, product=product).exists():
            return Response({"message": "이미 가입한 적금 상품입니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        option = get_object_or_404(SavingOptions, pk=option_id)

        SavingSubscription.objects.create(
            user=request.user, 
            product=product,
            saving_option=option, # 모델에 추가한 필드명과 일치해야 합니다
            amount=int(amount) # ✅ 가입 금액 저장
        )
        return Response({"message": "적금 상품 가입 완료"}, status=status.HTTP_201_CREATED)

    elif request.method == 'GET':
        subscription = SavingSubscription.objects.filter(user=request.user, product=product).first()
        serializer = SavingSubscriptionSerializer(subscription)
        return Response(serializer.data)

# user_all_subscriptions 뷰는 기존 로직을 그대로 유지해도 무방합니다. (Serializer가 데이터를 처리할 것이기 때문)

# 유저 페이지에서 전체 가입 목록을 가져올 때 사용할 뷰
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_all_subscriptions(request):
    deposit_subs = DepositSubscription.objects.filter(user=request.user)
    saving_subs = SavingSubscription.objects.filter(user=request.user)
    
    # [추가] 간단한 통계 데이터 계산
    # 예: 총 가입 상품 개수나 평균 금리 계산 가능
    total_count = deposit_subs.count() + saving_subs.count()
    
    d_serializer = DepositSubscriptionSerializer(deposit_subs, many=True)
    s_serializer = SavingSubscriptionSerializer(saving_subs, many=True)
    
    return Response({
        "username": request.user.username,
        "total_count": total_count,
        "deposits": d_serializer.data,
        "savings": s_serializer.data
    })

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deposit_unsubscribe(request, subscription_id):
    # 본인의 가입 내역만 삭제할 수 있도록 user=request.user 조건 추가
    subscription = get_object_or_404(DepositSubscription, id=subscription_id, user=request.user)
    subscription.delete()
    return Response({"message": "예금 가입이 해지되었습니다."}, status=status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def saving_unsubscribe(request, subscription_id):
    subscription = get_object_or_404(SavingSubscription, id=subscription_id, user=request.user)
    subscription.delete()
    return Response({"message": "적금 가입이 해지되었습니다."}, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def recommend_products(request):
    """
    LLM을 활용한 맞춤형 금융 상품 추천 뷰
    """
    # SSAFY GMS 엔드포인트 URL (curl 명령어 기준)
    url = "https://gms.ssafy.io/gmsapi/api.openai.com/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.OPENAI_API_KEY}"
    }

    # user = request.user

    dummy_profile = {
        "age": 28,
        "gender": "여성",
        "annual_income": 35000000,
        "tendency": "안정형",
        "asset": 5000000,
        "income": 3000000,
        "expense": 2500000,
        "top_spending_category": "식비",
        "spending_ratio": 40,
    }
    age = dummy_profile["age"]
    gender = dummy_profile["gender"]
    annual_income = dummy_profile["annual_income"]  
    tendency = dummy_profile["tendency"]
    asset = dummy_profile["asset"]
    income = dummy_profile["income"]
    expense = dummy_profile["expense"]
    top_spending_category = dummy_profile["top_spending_category"]
    spending_ratio = dummy_profile["spending_ratio"]

    user_content = f"""
    아래 고객 정보를 분석하여 최적의 상품을 추천해주세요.

    [고객 프로필]
    - 나이: {age}세
    - 성별: {gender}
    - 연 소득: {annual_income}원
    - 투자 성향: {tendency}
    - 현재 자산: {asset}원
    - 저축 여력: 월 {income - expense}원 (수입 {income} - 지출 {expense})
    - 주요 지출 내역: {top_spending_category} (전체 지출의 {spending_ratio}%)

    [추천 후보 상품 리스트 (DB 데이터)]
    1. [ID: 101] 우리은행 WON플러스예금 (금리 3.5%, 12개월)
    2. [ID: 105] 저축은행 특판 적금 (금리 4.5%, 6개월, 방문 가입 필수)
    3. [ID: 108] 카카오뱅크 자유적금 (금리 3.0%, 자유적립)

    위 후보 중 1개를 선택하고, 추가적인 투자 조언을 해주세요.

    [답변 예시]
    입력: (25세/사회초년생/여유자금 50만원/안정형)
    출력:
    {{
        "recommended_product_id": "108",
        "recommendation_reason": "사회초년생이라 목돈 마련이 우선입니다. 자유롭게 납입 가능한 카카오뱅크 적금으로 저축 습관을 기르는 것이 좋습니다.",
        "financial_advice": "현재 식비 지출이 40%로 높습니다. 배달 음식을 줄이면 월 20만 원을 더 저축할 수 있습니다.",
        "additional_category": "CMA 통장 (비상금 관리용)"
    }}

    이제 위 형식을 참고하여 실제 답변을 작성해주세요.
    """

    system_content = """
    당신은 '`FinMate'의 수석 AI 자산관리사입니다.
    금융 지식이 부족한 사회초년생부터 전문 투자자까지 다양한 고객에게 최적의 상품을 추천해야 합니다.

    [원칙]
    1. 분석은 논리적이어야 하며, 반드시 고객이 제공한 '가계부 데이터(수입/지출)'를 근거로 들어야 합니다.
    2. 말투는 신뢰감 있으면서도 친절한 '해요체'를 사용하세요.
    3. DB에 있는 상품을 추천할 때는 정확한 상품명을 언급하세요.
    4. 존재하지 않는 상품을 지어내지 마세요(Hallucination 방지).

    [출력 형식]
    답변은 반드시 아래 JSON 포맷을 따라주세요:
    {
        "recommended_product_id": "추천한 DB 상품의 ID (없으면 null)",
        "recommendation_reason": "추천 사유 (3문장 이내)",
        "financial_advice": "가계부 분석을 통한 재무 조언 (소비 습관 개선 제안 등)",
        "additional_category": "DB 외에 추천하는 투자 상품군 (예: ETF, 리츠)"
    }
    """

    data = {
        "model": "gpt-4.1-mini", 
        "messages": [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ],
        "max_tokens": 500,
        "temperature": 0.3
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        result = response.json()
        raw_recommendation = result['choices'][0]['message']['content']
        recommendation = json.loads(raw_recommendation)

        return Response({"recommendation": recommendation}, status=status.HTTP_200_OK)
    
    except requests.exceptions.RequestException as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)