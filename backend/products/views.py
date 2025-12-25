from django.shortcuts import get_object_or_404, get_list_or_404
from django.db.models import Sum
from datetime import date
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
import requests, json
from .models import DepositProducts, DepositOptions, SavingProducts, SavingOptions, DepositSubscription, SavingSubscription
from .serializers import DepositProductsSerializer, DepositOptionsSerializer, SavingProductsSerializer, SavingOptionsSerializer, DepositProductDetailSerializer, SavingProductDetailSerializer, DepositSubscriptionSerializer, SavingSubscriptionSerializer
from ledgers.models import Transaction

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
@permission_classes([IsAuthenticated])
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

    user = request.user

    # ---------------------------------------------------------
    # 1. [유저 프로필] UserProfile 모델에서 가져오기
    # ---------------------------------------------------------
    try:
        profile = user.profile
        # 모델의 @property age 활용 (없으면 30세 기본값)
        age = profile.age if profile.age else 30
        # 성별 (get_gender_display()를 쓰면 'Male'/'Female' 등 읽기 좋은 값으로 변환 가능)
        gender = profile.get_gender_display() if profile.gender else '알 수 없음'
        # 연 소득 (DB의 income 필드)
        annual_income = profile.income if profile.income else 0
        # 소비/투자 성향
        tendency = profile.spending_habits if profile.spending_habits else '분석 필요'
    except:
        # 프로필이 없는 경우 기본값
        age, gender, annual_income, tendency = 30, '알 수 없음', 0, '정보 없음'

    # ---------------------------------------------------------
    # 2. [자산 정보] 가계부 전체 내역으로 계산 (누적 자산)
    # ---------------------------------------------------------
    all_income = Transaction.objects.filter(user=user, category__type='INCOME').aggregate(Sum('amount'))['amount__sum'] or 0
    all_expense = Transaction.objects.filter(user=user, category__type='EXPENSE').aggregate(Sum('amount'))['amount__sum'] or 0
    current_asset = all_income - all_expense

    # ---------------------------------------------------------
    # 3. [이번 달 가계부] 소비 패턴 분석
    # ---------------------------------------------------------
    today = date.today()
    this_month_txs = Transaction.objects.filter(
        user=user, 
        date__year=today.year, 
        date__month=today.month
    )

    # 이번 달 수입/지출
    month_income = this_month_txs.filter(category__type='INCOME').aggregate(Sum('amount'))['amount__sum'] or 0
    month_expense = this_month_txs.filter(category__type='EXPENSE').aggregate(Sum('amount'))['amount__sum'] or 0
    
    # 여유 자금 (이번 달 저축 가능액)
    surplus_funds = month_income - month_expense

    # 지출 1위 카테고리 찾기
    top_spending = this_month_txs.filter(category__type='EXPENSE')\
        .values('category__name')\
        .annotate(total=Sum('amount'))\
        .order_by('-total')\
        .first()
    
    top_category = top_spending['category__name'] if top_spending else "없음"
    top_amount = top_spending['total'] if top_spending else 0
    spending_ratio = int((top_amount / month_expense * 100)) if month_expense > 0 else 0

    # ---------------------------------------------------------
    # 4. [추천 후보 상품] DB에서 가져오기
    # ---------------------------------------------------------
    # (1) 모든 예금 상품 가져오기
    all_deposits = DepositProducts.objects.all()
    deposit_list = []
    
    for p in all_deposits:
        # 해당 상품의 옵션 중 가장 높은 우대 금리 찾기
        options = DepositOptions.objects.filter(fin_prdt_cd=p)
        if options.exists():
            # intr_rate2가 없는 경우 0으로 처리
            max_rate = options.order_by('-intr_rate2').first().intr_rate2 or 0
        else:
            max_rate = 0
            
        deposit_list.append({
            'product': p,
            'max_rate': max_rate
        })
    
    # (2) 금리 내림차순 정렬 후 상위 5개 자르기
    deposit_list.sort(key=lambda x: x['max_rate'], reverse=True)
    top_5_deposits = deposit_list[:5]


    # (3) 모든 적금 상품 가져오기
    all_savings = SavingProducts.objects.all()
    saving_list = []
    
    for p in all_savings:
        options = SavingOptions.objects.filter(fin_prdt_cd=p, save_trm__in=[6,12,24,36])
        print(options)
        if options.exists():
            max_rate = options.order_by('-intr_rate2').first().intr_rate2 or 0
        else:
            max_rate = 0
            
        saving_list.append({
            'product': p,
            'max_rate': max_rate
        })
        
    # (4) 금리 내림차순 정렬 후 상위 5개 자르기
    saving_list.sort(key=lambda x: x['max_rate'], reverse=True)
    top_5_savings = saving_list[:5]


    # ---------------------------------------------------------
    # 문자열 생성 (프롬프트 입력용)
    product_list_str = "--- 예금 상품 (금리 상위 5개) ---\n"
    for item in top_5_deposits:
        p = item['product']
        rate = item['max_rate']
        product_list_str += f"- [ID:{p.id}] {p.fin_prdt_nm} ({p.kor_co_nm}) / 최고금리: {rate}%\n"

    product_list_str += "\n--- 적금 상품 (금리 상위 5개) ---\n"
    for item in top_5_savings:
        p = item['product']
        rate = item['max_rate']
        product_list_str += f"- [ID:{p.id}] {p.fin_prdt_nm} ({p.kor_co_nm}) / 최고금리: {rate}%\n"

    
    # dummy_profile = {
    #     "age": 28,
    #     "gender": "여성",
    #     "annual_income": 35000000,
    #     "tendency": "안정형",
    #     "asset": 5000000,
    #     "income": 3000000,
    #     "expense": 2500000,
    #     "top_spending_category": "식비",
    #     "spending_ratio": 40,
    # }
    # age = dummy_profile["age"]
    # gender = dummy_profile["gender"]
    # annual_income = dummy_profile["annual_income"]  
    # tendency = dummy_profile["tendency"]
    # asset = dummy_profile["asset"]
    # income = dummy_profile["income"]
    # expense = dummy_profile["expense"]
    # top_spending_category = dummy_profile["top_spending_category"]
    # spending_ratio = dummy_profile["spending_ratio"]
    
    

    # ---------------------------------------------------------
    # 5. [AI 프롬프트 구성]
    # ---------------------------------------------------------
    user_content = f"""
    아래 고객 데이터를 분석하여 가장 적합한 금융 상품 1개를 추천해주세요.

    [1. 고객 프로필]
    - 나이/성별: {age}세 / {gender}
    - 연 소득: {annual_income:,}원
    - 소비 성향: {tendency}
    - 현재 총 자산: {current_asset:,}원
    
    [2. 이번 달 가계부 현황]
    - 월 수입: {month_income:,}원
    - 월 지출: {month_expense:,}원
    - 월 여유 자금: {surplus_funds:,}원 (이 금액으로 저축 가능)
    - 최다 지출 항목: {top_category} (총 지출의 {spending_ratio}%)

    [3. 추천 후보 상품 리스트]
    {product_list_str}

    [요청 사항]
    위 후보 상품 중 고객의 상황(여유 자금, 소비 성향 등)에 가장 잘 맞는 상품 하나를 골라 추천해주세요.
    특히 '최다 지출 항목'을 언급하며 소비 습관에 대한 조언도 함께 해주세요.
    """

    system_content = """
    당신은 'FinMate'의 수석 AI 자산관리사입니다.

    [원칙]
    1. 반드시 제공된 [추천 후보 상품 리스트] 내에 있는 상품 중 하나를 골라 추천해야 합니다.
    2. 없는 상품을 지어내지 마세요.
    3. 추가 투자 제안에는 이유도 포함하세요.
    4. JSON 형식으로만 응답하세요.
    5. 응답 형식은 반드시 아래 예시를 따르세요.

    [출력 JSON 포맷]
    {
        "recommended_product_id": "추천 상품 ID (숫자)",
        "product_type": "예금 또는 적금",
        "recommendation_reason": "추천 이유 (고객의 소득, 여유 자금 등을 구체적으로 언급)",
        "financial_advice": "재무 조언 (예: 식비가 많으니 줄이세요, 여유 자금은 적금으로 등)",
        "additional_category": "DB 상품 외 추천 투자처 (예: ETF, CMA, 채권 등)"
    }
    """

    data = {
        "model": "gpt-5.2", 
        "messages": [
            {"role": "developer", "content": system_content},
            {"role": "user", "content": user_content}
        ],
        "temperature": 0.3
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        result = response.json()
        raw_recommendation = result['choices'][0]['message']['content']

        # JSON 파싱 (마크다운 ```json ... ``` 제거)
        clean_json = raw_recommendation.replace("```json", "").replace("```", "").strip()
        recommendation = json.loads(clean_json)

        return Response({"recommendation": recommendation}, status=status.HTTP_200_OK)
    
    except requests.exceptions.RequestException as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)